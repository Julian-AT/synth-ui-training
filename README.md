# SynthUI Dataset & Training

## This repo contains all business logic for the following pipelines

- Scraping raw code from GitHub
- Filtering out irrelevant code
- Preperation for HuggingFace Dataset (Tokenization, Dedupe, etc.)
- Generation of QA pairs
- Pushing to HuggingFace Dataset

## Dataset Generation

### Resulting Dataset

- [JulianAT/SynthUI-Code-2k-v1](https://huggingface.co/datasets/JulianAT/SynthUI-Code-2k-v1)
- [JulianAT/SynthUI-Code-Instruct-2k-v1](https://huggingface.co/datasets/JulianAT/SynthUI-Code-Instruct-2k-v1)

### How to use

#### Create dataset with raw code snippets

1. Go to https://github.com/settings/tokens and create new token by clicking `Generate New Token` button. Give read access to public repositories.

2. Copy the access token and set the env variable via `export 
GH_ACCESS_TOKEN=<copied access token>`.

3. `cd dataset_creation` and run `python clone_hf_repos.py`

4. The data in `synth_source_repos` should look like this:

   ```shell
   alifarooq9/rapidlaunch  DarkInventor/easy-ui  horizon-ui/shadcn-nextjs-boilerplate  ixartz/SaaS-Boilerplate  lucide-icons/lucide  moinulmoin/chadnext  nobruf/shadcn-landing-page  shadcn-ui/taxonomy
   ```

5. Download nltk punkt

   ```python
   import nltk
   nltk.download('punkt')
   ```

6. Run Data Pipeline on a machine with 16 CPUs:

   ```shell
   python pipeline.py
   ```

7. Collate and push to HF hub:

   ```shell
   python prepare_hf_dataset.py
   ```

#### Create dataset with QA pairs (existing raw dataset is required)

1. Go to https://huggingface.co/settings/tokens and create a new token by clicking `Create new token` button. Select the `read` scope and click `Create token`.
2. Copy the access token and set the env variable via `export HF_TOKEN=<copied access token>`.
3. `cd dataset_creation` and run `python generate_qa_pairs.py`. (this will take a while)
4. Run `push_qa_pairs.py` to push the dataset to the HuggingFace Hub.

#### The dataset contains data scraped from following github repos

```python
ICON_REPOS = [
    "lucide-icons/lucide"                               # ISC
]
UI_REPOS = [
    "shadcn-ui/ui",                                     # MIT
    "DarkInventor/easy-ui"                              # MIT
]
CODE_REPOS = [
    "moinulmoin/chadnext",                              # MIT
    "shadcn-ui/taxonomy",                               # MIT
    "horizon-ui/shadcn-nextjs-boilerplate",             # MIT
    "alifarooq9/rapidlaunch",                           # MIT
    "ixartz/SaaS-Boilerplate",                          # MIT
    "nobruf/shadcn-landing-page"                        # None
]
```

## Training

The datasets (especially the QA dataset) are ment to fine-tune instruction models. Great examples for resulting models are `Octocoder` or `StarChat`.

> **Note**: Since the resources for this project were limited, the fine-tuning is optimized to run on **a single A100 GPU** with the highest RAM settings on Colab.

### Resources

1. Codebase: The codebase uses `Flash Attention V2` support in Transformers.
2. [Colab Notebook](): Minimum one A100 GPU is required.
3. Model to be fine-tuned: [bigcode/starcoderplus](https://huggingface.co/bigcode/starcoderplus)
4. Dataset: [JulianAT/SynthUI-Code-Instruct-2k-v1](https://huggingface.co/datasets/JulianAT/SynthUI-Code-Instruct-2k-v1)
5. Trained Model: [JulianAT/StarCoder-Plus-SynthUI-Code-Instruct-2k-v1](https://huggingface.co/JulianAT/StarCoder-Plus-SynthUI-Code-Instruct-2k-v1)

## Epilogue

This project was done as a proof of concept for the potential of fine-tuning instruction models with synthetic data. For the scope of this project the synthetic data was scraped from GitHub. However, the approach can be easily replicated with other data sources.

The resulting model was used for code generation in the [WebApp of Synth UI](https://www.synthui.design/).
