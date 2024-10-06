# coding=utf-8
# NOTE: The logger will throw encoding errors. This does not affect the pipeline execution.


from datatrove.executor.base import PipelineExecutor
from datatrove.executor.local import LocalPipelineExecutor
from datatrove.pipeline.dedup import MinhashDedupSignature
from datatrove.pipeline.dedup.minhash import (
    MinhashConfig,
    MinhashDedupBuckets,
    MinhashDedupCluster,
    MinhashDedupFilter,
)
from datatrove.pipeline.tokens import TokensCounter
from datatrove.pipeline.readers import JsonlReader
from datatrove.pipeline.writers.jsonl import JsonlWriter
from reader import SynthUIDatasetReader
from filter import BasicCodeFilter
from loguru import logger
import sys

MIRROR_DIRECTORY = "synth_source_repos"
TOTAL_TASKS = 16

sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
logger.add("logs.log", encoding="utf-8")

output_folder_prefix = "pipeline_output"

# you can also change ngrams or the number of buckets and their size here
minhash_config = MinhashConfig(
    use_64bit_hashes=True
)  # better precision -> fewer false positives (collisions)


def run_code_dataset_generation():
    # stage 0 reads the code data and does basic filtering
    pipeline_0 = [
        SynthUIDatasetReader(data_folder=MIRROR_DIRECTORY),
        BasicCodeFilter(),
        JsonlWriter(output_folder=f"{output_folder_prefix}/filtered_data"),
    ]

    # stage 1 computes minhash signatures for each task (each task gets a set of files)
    pipeline_1 = [
        JsonlReader(f"{output_folder_prefix}/filtered_data"),
        MinhashDedupSignature(
            output_folder=f"{output_folder_prefix}/signatures",
            config=minhash_config,
        ),
    ]

    # stage 2 finds matches between signatures in each bucket
    pipeline_2 = [
        MinhashDedupBuckets(
            input_folder=f"{output_folder_prefix}/signatures",
            output_folder=f"{output_folder_prefix}/buckets",
            config=minhash_config,
        ),
    ]

    # stage 3 creates clusters of duplicates using the results from all buckets
    pipeline_3 = [
        MinhashDedupCluster(
            input_folder=f"{output_folder_prefix}/buckets",
            output_folder=f"{output_folder_prefix}/remove_ids",
            config=minhash_config,
        ),
    ]

    # stage 4 reads the original input data and removes all but 1 sample per duplicate cluster
    # the data must match exactly stage 1, so number of tasks and the input source must be the same
    pipeline_4 = [
        JsonlReader(f"{output_folder_prefix}/filtered_data"),
        TokensCounter(),  # nice way to see how many tokens we had before and after deduplication
        MinhashDedupFilter(
            input_folder=f"{output_folder_prefix}/remove_ids",
            exclusion_writer=JsonlWriter(f"{output_folder_prefix}/removed"),
        ),
        JsonlWriter(output_folder="synth_ui_data"),
    ]

    executor_0: PipelineExecutor = LocalPipelineExecutor(
        pipeline=pipeline_0, tasks=TOTAL_TASKS, start_method="spawn"
    )

    executor_1: PipelineExecutor = LocalPipelineExecutor(
        pipeline=pipeline_1, tasks=TOTAL_TASKS, start_method="spawn"
    )

    executor_2: PipelineExecutor = LocalPipelineExecutor(
        pipeline=pipeline_2,
        tasks=minhash_config.num_buckets,
        start_method="spawn"
    )

    executor_3: PipelineExecutor = LocalPipelineExecutor(pipeline=pipeline_3, tasks=1, start_method="spawn")

    executor_4: PipelineExecutor = LocalPipelineExecutor(
        pipeline=pipeline_4, tasks=TOTAL_TASKS, start_method="spawn"
    )

    print(executor_0.run())
    print(executor_1.run())
    print(executor_2.run())
    print(executor_3.run())
    print(executor_4.run())


if __name__ == "__main__":
    run_code_dataset_generation()
