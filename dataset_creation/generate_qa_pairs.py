import pandas as pd
import openai
import time
import json
from tqdm import tqdm

# OpenAI API key
openai.api_key = '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'

# Load the DataFrame
df = pd.read_parquet("hf://datasets/JulianAT/SynthUI-Code-2k-v1/data/train-00000-of-00001.parquet")
# df = df.head(10)  # Limiting to 10 rows for testing

# Function to generate a question using the OpenAI API
def generate_question(text):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {
                    "role": "system",
                    "content": """You are a QA engineer at a software company. You are working on a dataset with NextJS code snippets and their corresponding instructions for a QA dataset.
                    
                    It's your task to generate synthetic instructions of code-snippets for a QA dataset. The code-snippets you will receive are scraped from the most popular NextJS repositories on GitHub.
                    
                    The focus should be on NextJS. UI components, routing, and state management are the main topics.
                    
                    You will need to generate fitting instructions with that a LLM would be able to generate the code-snippet. The instructions should be as clear and concise as possible.
                    ONLY output instructions as plain text without any extra decorators."""
                },
                {
                    "role": "user",
                    "content": f"Code Snippet: {text}"
                }
            ],
            temperature=0.7
        )
        question = response.choices[0].message.content
        return question
    except Exception as e:
        print(f"Error generating QA Pair: {e}")
        return None

# List to store QA pairs
qa_pairs = []

# Iterate through each row of the DataFrame with tqdm for progress tracking
for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing QA pairs"):
    text = row['text']
    metadata = row["metadata"]
    question = generate_question(text)
    
    # Append the generated QA pair to the list
    if question:
        qa_pairs.append({"instruction": question, "output": text, "metadata": metadata})
    
    # 20ms delay to avoid rate limiting => ~80 requests per second
    time.sleep(0.02)

# Save the QA pairs to a JSON file
with open("qa_pairs.json", "w", encoding='utf-8') as json_file:
    json.dump(qa_pairs, json_file, ensure_ascii=False, indent=4)

print("Successfully saved QA Pairs to 'qa_pairs.json'.")
