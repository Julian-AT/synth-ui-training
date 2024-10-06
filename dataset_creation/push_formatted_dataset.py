import pandas as pd
from prepare_hf_dataset import push_hf_dataset

df = pd.read_csv("train_format/reformatted_dataset.csv")
push_hf_dataset(df, "JulianAT/SynthUI-Code-Chat-Assistant-v1")