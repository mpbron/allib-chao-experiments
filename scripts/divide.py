from pathlib import Path
from typing import List, Sequence, Tuple
import shutil

from allib.utils.io import create_dir_if_not_exists
from allib.benchmarking.datasets import (
    DatasetType,
    TrecDatasetAL,
    ReviewDatasets,
    detect_type,
)
from allib.configurations.catalog import ExperimentCombination

import argparse
import stat

SMALL_MAX = 15000
LARGE_MAX = 50000
PREVALENCE_MIN = 10
SIZE_MIN = 500
EXPERIMENTS_LOW_MEMORY = (
    ExperimentCombination.AUTOTAR,
    ExperimentCombination.CHAO,
    ExperimentCombination.CMH,
    ExperimentCombination.TARGET,
)
EXPERIMENTS_HIGH_MEMORY = (ExperimentCombination.AUTOSTOP,)

EXPERIMENTS_LOW_MEMORY_FILENAME = "experiments_low_memory.txt"
EXPERIMENTS_HIGH_MEMORY_FILENAME = "experiments_high_memory.txt"

SMALL = "topics_small"
LARGE = "topics_large"
XLARGE = "topics_xlarge"

BASE_SCRIPTS = [
    "benchmark_review.sh",
    "benchmark_trec.sh",
    "create_review_jobs.sh",
    "create_trec_jobs.sh"
]

DEFAULT_REVIEW = "./benchmark_review.sh"
DEFAULT_TREC = "./benchmark_trec.sh"

def divide_datasets(
    source_path: Path,
    jobpath: Path,
    dstype: DatasetType,
    pos_label: str,
    name: str = "",
    small_max=SMALL_MAX,
    large_max=LARGE_MAX,
    prevalence_min=PREVALENCE_MIN,
    size_min=SIZE_MIN,
) -> Tuple[Sequence[str], Sequence[str], Sequence[str]]:
    dss_name = name if name else source_path.stem
    dstype = detect_type(source_path)
    small_path = jobpath / f"{SMALL}_{dss_name}.txt"
    large_path = jobpath / f"{LARGE}_{dss_name}.txt"
    xlarge_path = jobpath / f"{XLARGE}_{dss_name}.txt"
    if dstype == DatasetType.REVIEW:
        dss = ReviewDatasets.from_path(source_path)
    else:
        dss = TrecDatasetAL.from_path(source_path)
    small_topics: List[str] = list()
    large_topics: List[str] = list()
    xlarge_topics: List[str] = list()
    for topic in dss.topic_keys:
        env = dss.get_env(topic)
        size = len(env.dataset)
        size_pos = env.truth.document_count(pos_label)
        if size_pos > prevalence_min and size >= size_min:
            if size < small_max:
                small_topics.append(topic)
            elif size < large_max:
                large_topics.append(topic)
            else:
                xlarge_topics.append(topic)
    with small_path.open("w") as fh:
        fh.write("\n".join(small_topics))
    with large_path.open("w") as fh:
        fh.write("\n".join(large_topics))
    with xlarge_path.open("w") as fh:
        fh.write("\n".join(xlarge_topics))
    return small_topics, large_topics, xlarge_topics


def write_experiments_files(
    jobpath: Path,
    low_exps: Sequence[ExperimentCombination] = EXPERIMENTS_LOW_MEMORY,
    high_exps: Sequence[ExperimentCombination] = EXPERIMENTS_HIGH_MEMORY,
):
    low_path = jobpath / EXPERIMENTS_LOW_MEMORY_FILENAME
    high_path = jobpath / EXPERIMENTS_HIGH_MEMORY_FILENAME
    with low_path.open("w") as fh:
        fh.write("\n".join(low_exps))
    with high_path.open("w") as fh:
        fh.write("\n".join(high_exps))

def copy_scripts(jobpath: Path) -> None:
    targets = [(jobpath / script) for script in BASE_SCRIPTS]
    source = Path.cwd() if Path.cwd().stem == "scripts" else Path.cwd() / "scripts"
    if source.exists():
        sources = [(source/ script) for script in BASE_SCRIPTS]
        for (sf, tf) in zip(sources, targets):
            shutil.copy(sf, tf)


def create_jobs(
    path: Path,
    target_path: Path,
    jobpath: Path,
    pos_label: str,
    name: str = "",
    small_max=SMALL_MAX,
    large_max=LARGE_MAX,
    prevalence_min=PREVALENCE_MIN,
    test_iterations=30,
    high_cpu: int = 40,
    medium_cpu: int = 20,
    low_cpu: int = 2,
    trec_cmd: str = DEFAULT_REVIEW,
    review_cmd: str = DEFAULT_TREC,
) -> Path:
    create_dir_if_not_exists(jobpath)
    write_experiments_files(jobpath)
    copy_scripts(jobpath)
    exp_low_path = (jobpath / EXPERIMENTS_LOW_MEMORY_FILENAME).resolve()
    exp_high_path = (jobpath / EXPERIMENTS_HIGH_MEMORY_FILENAME).resolve()
    dstype = detect_type(path)
    dss_name = name if name else path.stem
    ds_job = jobpath / f"job_{dss_name}.sh"
    sj, lj, xlj = divide_datasets(
        path, jobpath, dstype, pos_label, name, small_max, large_max, prevalence_min
    )
    small_path = (jobpath / f"{SMALL}_{dss_name}.txt").resolve()
    large_path = (jobpath / f"{LARGE}_{dss_name}.txt").resolve()
    xlarge_path = (jobpath / f"{XLARGE}_{dss_name}.txt").resolve()
    cmd = trec_cmd if dstype == DatasetType.TREC else review_cmd
    sp = path.resolve()
    tp = target_path.resolve()
    cmds = [
        """#!/bin/bash""",
        f"{cmd} {sp} {small_path} {tp} {exp_low_path} {test_iterations} {high_cpu}",
        f"{cmd} {sp} {small_path} {tp} {exp_high_path} {test_iterations} {medium_cpu}",
        f"{cmd} {sp} {large_path} {tp} {exp_low_path} {test_iterations} {medium_cpu}",
        f"{cmd} {sp} {large_path} {tp} {exp_high_path} {test_iterations} {low_cpu}",
        f"{cmd} {sp} {xlarge_path} {tp} {exp_low_path} {test_iterations} {medium_cpu}",
        f"{cmd} {sp} {xlarge_path} {tp} {exp_high_path} {test_iterations} {low_cpu}",
    ]
    with ds_job.open("w") as fh:
        fh.write("\n".join(cmds))
    ds_job.chmod(ds_job.stat().st_mode | stat.S_IEXEC)
    return ds_job

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="allib", description="Active Learning Library (allib) - Benchmarking tool"
    )
    parser.add_argument("-j", "--jobpath", help="Path of jobfiles", type=Path)
    parser.add_argument("-d", "--dataset", help="The path to the dataset", type=Path)
    parser.add_argument("-n", "--name", help="The name of the dataset", type=str)
    parser.add_argument("-t", "--target", help="The target of the results", type=Path)
    parser.add_argument('--iterations', type=int, default=30)
    parser.add_argument("--lowmemcpu", type=int, default=8)
    parser.add_argument("--highmemcpu", type=int, default=2)
    parser.add_argument("--mediummemcpu", type=int, default=4)
    parser.add_argument("--reviewcmd", type=str, default=DEFAULT_REVIEW)
    parser.add_argument("--treccmd", type=str, default=DEFAULT_TREC)
    parser.add_argument("--pos_label", metavar="POS", default="Relevant",
        help="The label that denotes the positive class",
    )
    args = parser.parse_args()
    job_path = create_jobs(
        args.dataset,
        args.target,
        args.jobpath,
        args.pos_label,
        name=args.name,
        high_cpu=args.lowmemcpu,
        medium_cpu=args.mediummemcpu,
        low_cpu=args.highmemcpu,
        review_cmd=args.reviewcmd,
        trec_cmd=args.treccmd,
        test_iterations=args.iterations
    )
    print(str(job_path))
