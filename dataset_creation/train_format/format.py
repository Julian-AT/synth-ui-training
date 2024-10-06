from datasets import load_dataset
import pandas as pd

ds = load_dataset("JulianAT/SynthUI-Code-Instruct-2k-v1", split="train")

def reformat(row):
    instruction = row["instruction"]
    output = row["output"]
    
    formatted_row = (f"<|system|> You are a helpful, respectful and honest assistant. "
                         "Always answer as helpfully as possible, while being safe. "
                         "Your answers should not include any harmful, unethical, racist, sexist, "
                         "toxic, dangerous, or illegal content. Please ensure that your responses are "
                         "socially unbiased and positive in nature. If a question does not make any sense, "
                         "or is not factually coherent, explain why instead of answering something not correct. "
                         "If you don't know the answer to a question, please don't share false information. "
                         "<|endoftext|> <|prompter|> [INSTRUCTION] <|endoftext|> <|assistant|> [OUTPUT] <|endoftext|>")
    
    formatted_row = formatted_row.replace("[INSTRUCTION]", instruction)
    formatted_row = formatted_row.replace("[OUTPUT]", output)
    
    return {"formatted_row": formatted_row}

formatted_data = ds.map(reformat)
new_df = pd.DataFrame({"content": formatted_data["formatted_row"]})

new_df.to_csv("reformatted_dataset.csv", index=False)