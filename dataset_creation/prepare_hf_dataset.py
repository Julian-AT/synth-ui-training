# coding=utf-8
# Copyright 2024 Sourab Mangrulkar. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pandas as pd
import gzip
import json
from datasets import Dataset

DATAFOLDER = "synth_ui_data"
HF_DATASET_NAME = "JulianAT/SynthUI-Code-2k-v1"


def load_gzip_jsonl(file_path):
    data = []
    with gzip.open(file_path, "rt", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))
    return data


def create_hf_dataset():
    df = None
    for file in os.listdir(DATAFOLDER):
        data = load_gzip_jsonl(os.path.join(DATAFOLDER, file))
        if df is None:
            df = pd.DataFrame(data)
        else:
            df = pd.concat([df, pd.DataFrame(data)])

    push_hf_dataset(df, HF_DATASET_NAME)
    
def push_hf_dataset(df: pd.DataFrame, dataset_name: str):
    dataset = Dataset.from_pandas(df)
    dataset = dataset.train_test_split(test_size=0.15)
    print(os.environ.get("HF_TOKEN"))
    dataset.push_to_hub(dataset_name, private=False, token=os.environ.get("HF_TOKEN"))


if __name__ == "__main__":
    create_hf_dataset()
