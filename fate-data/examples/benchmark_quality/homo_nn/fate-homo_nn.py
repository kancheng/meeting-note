#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import argparse
import torch as t
from pipeline import fate_torch_hook
from pipeline.backend.pipeline import PipeLine
from pipeline.component import DataTransform, HomoNN, Evaluation
from pipeline.component import Reader
from pipeline.interface import Data, Model
from pipeline.utils.tools import load_job_config, JobConfig
from federatedml.evaluation.metrics import classification_metric
from fate_test.utils import extract_data, parse_summary_result
from pipeline.component.nn import TrainerParam, DatasetParam


fate_torch_hook(t)


class dataset(object):
    breast = {
        "guest": {"name": "breast_homo_guest", "namespace": "experiment"},
        "host": [
            {"name": "breast_homo_host", "namespace": "experiment"},
            {"name": "breast_homo_host", "namespace": "experiment"}
        ]
    }
    vehicle = {
        "guest": {"name": "vehicle_scale_homo_guest", "namespace": "experiment"},
        "host": [
            {"name": "vehicle_scale_homo_host", "namespace": "experiment"},
            {"name": "vehicle_scale_homo_host", "namespace": "experiment"}
        ]
    }


def main(config="../../config.yaml", param="param_conf.yaml", namespace=""):
    num_host = 1
    if isinstance(config, str):
        config = load_job_config(config)

    if isinstance(param, str):
        param = JobConfig.load_from_file(param)

    epoch = param["epoch"]
    lr = param["lr"]
    batch_size = param.get("batch_size", -1)
    is_multy = param["is_multy"]
    data = getattr(dataset, param.get("dataset", "vehicle"))

    if is_multy:
        loss = t.nn.CrossEntropyLoss()
    else:
        loss = t.nn.BCELoss()

    input_shape = 18 if is_multy else 30
    output_shape = 4 if is_multy else 1
    out_act = t.nn.Softmax(dim=1) if is_multy else t.nn.Sigmoid()

    model = t.nn.Sequential(
        t.nn.Linear(input_shape, 16),
        t.nn.ReLU(),
        t.nn.Linear(16, output_shape),
        out_act
    )

    optimizer = t.optim.Adam(model.parameters(), lr=lr)

    guest_train_data = data["guest"]
    host_train_data = data["host"][:num_host]
    for d in [guest_train_data, *host_train_data]:
        d["namespace"] = f"{d['namespace']}{namespace}"

    hosts = config.parties.host[:num_host]

    pipeline = PipeLine() .set_initiator(
        role='guest',
        party_id=config.parties.guest[0]) .set_roles(
        guest=config.parties.guest[0],
        host=hosts,
        arbiter=config.parties.arbiter)

    reader_0 = Reader(name="reader_0")
    reader_0.get_party_instance(
        role='guest',
        party_id=config.parties.guest[0]).component_param(
        table=guest_train_data)
    for i in range(num_host):
        reader_0.get_party_instance(role='host', party_id=hosts[i]) \
            .component_param(table=host_train_data[i])

    data_transform_0 = DataTransform(name="data_transform_0", with_label=True)
    data_transform_0.get_party_instance(
        role='guest', party_id=config.parties.guest[0]) .component_param(
        with_label=True, output_format="dense")
    data_transform_0.get_party_instance(
        role='host',
        party_id=hosts).component_param(
        with_label=True)

    if is_multy:
        ds_param = DatasetParam(
            dataset_name='table',
            flatten_label=True,
            label_dtype='long')
    else:
        ds_param = DatasetParam(dataset_name='table')

    homo_nn_0 = HomoNN(
        name="homo_nn_0",
        trainer=TrainerParam(
            trainer_name='fedavg_trainer',
            epochs=epoch,
            batch_size=batch_size,
        ),
        dataset=ds_param,
        torch_seed=100,
        optimizer=optimizer,
        loss=loss,
        model=model)
    homo_nn_1 = HomoNN(name="homo_nn_1")

    if is_multy:
        eval_type = "multi"
    else:
        eval_type = "binary"
    evaluation_0 = Evaluation(
        name='evaluation_0',
        eval_type=eval_type,
        metrics=[
            "accuracy",
            "precision",
            "recall"])

    pipeline.add_component(reader_0)
    pipeline.add_component(
        data_transform_0, data=Data(
            data=reader_0.output.data))
    pipeline.add_component(homo_nn_0, data=Data(
        train_data=data_transform_0.output.data))
    pipeline.add_component(
        homo_nn_1, data=Data(
            test_data=data_transform_0.output.data), model=Model(
            homo_nn_0.output.model))
    pipeline.add_component(evaluation_0, data=Data(data=homo_nn_0.output.data))
    pipeline.compile()
    pipeline.fit()

    metric_summary = parse_summary_result(
        pipeline.get_component("evaluation_0").get_summary())
    nn_0_data = pipeline.get_component("homo_nn_0").get_output_data()
    nn_1_data = pipeline.get_component("homo_nn_1").get_output_data()
    nn_0_score = extract_data(nn_0_data, "predict_result")
    nn_0_label = extract_data(nn_0_data, "label")
    nn_1_score = extract_data(nn_1_data, "predict_result")
    nn_1_label = extract_data(nn_1_data, "label")
    nn_0_score_label = extract_data(nn_0_data, "predict_result", keep_id=True)
    nn_1_score_label = extract_data(nn_1_data, "predict_result", keep_id=True)

    if eval_type == "binary":
        # metric_nn = {
        #     "score_diversity_ratio": classification_metric.Distribution.compute(nn_0_score_label, nn_1_score_label),
        #     "ks_2samp": classification_metric.KSTest.compute(nn_0_score, nn_1_score),
        #     "mAP_D_value": classification_metric.AveragePrecisionScore().compute(nn_0_score, nn_1_score, nn_0_label,
        #                                                                          nn_1_label)}
        # metric_summary["distribution_metrics"] = {"homo_nn": metric_nn}
        if metric_summary is None:
            metric_summary = {}
        metric_summary["accuracy"] = (
            nn_0_score == nn_0_label).sum() / len(nn_0_label)
    # elif eval_type == "multi":
    #     metric_nn = {
    #         "score_diversity_ratio": classification_metric.Distribution.compute(nn_0_score_label, nn_1_score_label)}
    #     metric_summary["distribution_metrics"] = {"homo_nn": metric_nn}

    data_summary = dict(
        train={"guest": guest_train_data["name"], **{f"host_{i}": host_train_data[i]["name"] for i in range(num_host)}},
        test={"guest": guest_train_data["name"], **{f"host_{i}": host_train_data[i]["name"] for i in range(num_host)}}
    )

    return data_summary, metric_summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser("BENCHMARK-QUALITY PIPELINE JOB")
    parser.add_argument("-config", type=str,
                        help="config file")
    parser.add_argument("-param", type=str,
                        help="config file for params")
    args = parser.parse_args()
    if args.config is not None:
        main(args.config, args.param)
    else:
        main(args.param)
