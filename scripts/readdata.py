from pathlib import Path
import pickle
import argparse
from allib.analysis.summarize import read_results_memsafe

def transform_results(source: Path, target: Path) -> None:
  df = read_results_memsafe(source)
  with target.open("wb") as fh:
    pickle.dump(df, fh)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="allib", description="Active Learning Library (allib) - Benchmarking tool"
    )
    parser.add_argument("-s", "--source", type=Path)
    parser.add_argument("-t", "--target", type=Path)
    args = parser.parse_args()
    transform_results(args.source, args.target)