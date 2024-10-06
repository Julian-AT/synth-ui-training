import pandas as pd
from prepare_hf_dataset import push_hf_dataset

df = pd.read_json("qa_pairs.json")
push_hf_dataset(df, "JulianAT/SynthUI-Code-Instruct-2k-v1")