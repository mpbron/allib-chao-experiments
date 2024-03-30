# Using Chao’s Estimator as a Stopping Criterion for TAR

M.P. Bron, P.G.M. van der Heijden, A.J. Feelders, A.P.J.M. Siebes

------------------------------------------------------------------------

In this repository, we publish the code that was used to perform the
experiments in our paper. In our work, we used our library
[`python-allib`](https://github.com/mpbron/python-allib) to perform the
experiment in our study. Specifically, we use version `0.5.1`, stored
[here](https://doi.org/10.5281/zenodo.10869848) \[1\]. The library
`python-allib` itself is also usable for other purposes. This repository
is intended to show our work on our stopping criterion simulation study
and enable the reader to reproduce the results of our experiments.

## Installation

Clone the repository on your system (using `git clone ...`) or download
it as a zip archive.

## Download the datasets

In our experiments, we used the following studies as benchmark data: We
included the following datasets in our study:

- [CLEF2017](https://npai.science.uu.nl/clefdatasets/clef2017.zip)
- [CLEF2018](https://npai.science.uu.nl/clefdatasets/clef2018.zip)
- [CLEF2019](https://npai.science.uu.nl/clefdatasets/clef2019.zip)
- [SYNERGY](https://github.com/asreview/synergy-dataset)

The CLEF datasets were originally provided by \[3\] on their
[repository](https://github.com/dli1/auto-stop-tar), however, the data
is no longer available from the link they provided, unfortunately.
Therefore, we decided to make the data available again to make our
experiments and results reproducible. The data is stored as a ZIP
archive, and should be extracted at a location of your choosing. Besides
the CLEF data, we used datasets from
[SYNERGY](https://github.com/asreview/synergy-dataset) \[2\] in our
experiments. Use the SYNERGY Python package to retrieve the datasets.

## Experiments (directly on your own system)

### System Requirements

You need a system with the following specifications:

- A Linux system (e.g., Ubuntu 22.04 LTS). Other systems may work;
  however, this has not been tested. If you are on Windows, consider
  using WSL2 with a Ubuntu 22.04 installation.

- Python 3.8 or higher, we performed our experiments on Python 3.10.

- Install the Python requirements found in `requirements.txt` in a
  *virtual environment*. You can create one with the following command:
  `python3 -m venv .venv`. You may have to use `python` instead of
  `python3` or install some packages on your system. If you use Ubuntu,
  your system will indicate this. After activating your virtual
  environment, you can install the requirements by executing
  `pip install -r requirements.txt`.

- R 3.6 or higher with the following packages

  - `tidyverse`

  - `RCapture`

- GNU Parallel for parallelization of the experiments (Can be installed
  on Ubuntu by issuing `sudo apt install parallel`)

To run the experiments for the AUTOSTOP algorithm \[3\], a considerable
amount of RAM is needed when applying it to large datasets. For a
dataset of 15000 documents, 20 GB of RAM is needed, and memory
consumption grows quadratically in terms of dataset size.

### Run the benchmark experiments

You can perform a single experiment with the following commands:

For a CSV from SYNERGY:

``` console
$ python -m allib benchmark -m Review -d  ./path/to/dataset -t ./path/to/results/ -e AUTOTAR -r 42
```

For a dataset in TREC-style (e.g., CLEF) use the following command. Note
that you have to supply the TOPIC code.

``` console
$ python -m allib benchmark -m Trec -d  ./path/to/dataset/ -i TOPIC -t ./path/to/results/ -e AUTOTAR -r 42
```

We can use the following script to run a large scale on a dataset
folder. In this repository, it can be found under the name
`run_benchmark.sh`.

``` bash
#!/bin/bash
echo "Reading path $1 as dataset"
echo "Setting $2 as dataset name"
echo "Selecting path $3 as result target"
echo "Selecting path $4 as job target"
echo "Repeating each method with $5 different seed sets"
echo "Executing jobs with Low memory requirements with $6 CPU cores"
echo "Executing jobs with Medium memory requirements wth $7 CPU cores"
echo "Executing jobs with High memory requirements with $8 CPU cores"
python3 divide.py -d $1 -n $2 -t $3 -j $4 --iterations $5 --lowmemcpu $6 --mediummemcpu $7 --highmemcpu $8
cd $4
jobname="job_$2.sh"
jobpath="./$jobname"
echo "Starting experiments"
sh $jobpath
```

Then, this script can be invoked as follows:

``` console
$ ./run_benchmark.sh /data/tardata/clef2019 clef2019 ./results ./jobs 1 8 4 1 
Reading path /data/tardata/clef2019 as dataset
Setting clef2019 as dataset name
Selecting path ./results as result target
Selecting path ./jobs as job target
Repeating each method with 1 different seed sets
Executing jobs with Low memory requirements with 8 CPU cores
Executing jobs with Medium memory requirements wth 4 CPU cores
Executing jobs with High memory requirements with 1 CPU cores
```

We repeated each experiment with 30 seed sets. As the individual
experiments can run concurrently, we use GNU Parallel to speed up the
process. We executed our experiments on a machine with 512 GB of RAM and
48 CPU cores with the below commands. We advise you to adjust the core
parameters to meet the specifications of your machine.

``` console
$ ./run_benchmark.sh /path/to/synergy synergy ./results/synergy ./jobs 30 40 20 1
$ ./run_benchmark.sh /path/to/clef2017 clef2017 ./results/clef2017 ./jobs 30 40 20 1
$ ./run_benchmark.sh /path/to/clef2018 clef2018 ./results/clef2018 ./jobs 30 40 20 1
$ ./run_benchmark.sh /path/to/clef2019 clef2018 ./results/clef2019 ./jobs 30 40 20 1
```

## Experiments in a container

Besides running the code directly on your Ubuntu machine, you can also
run the experiments in a container. Running the code in a container has
the benefit that you do not have to install all dependencies yourself.
For example, configuring `R` on Linux can be a hassle, and this is
already fixed for you within the container. To use the container method,
install a container framework (e.g., `docker` or `podman`). We recommend
using `podman` if you are new to containers, as this is easier to
install. On Ubuntu 22.04 and above, you can install `podman` by
executing `sudo apt install podman`. You can also run `podman` and
`docker` on Windows and macOS. Once installed, you can issue the
following command to build the container. Your current working directory
should be the root of this repository.

``` console
$ podman build -t allib-chao .
# OR
$ docker build -t allib-chao .
```

This command will build the container using the
[`Dockerfile`](Dockerfile). This container is based on a Ubuntu 22.04
LTS image, which already contains a working R installation. After
building has succeeded, you can run the `run_benchmark_podman.sh` or
`run_benchmark_docker.sh` script, which takes arguments in the same
order as the `run_benchmark` script:

``` console
$ ./run_benchmark_podman.sh /data/tardata/clef2018 clef2018 ./results/ ./jobs 30 8 4 1
Reading path /data/tardata/clef2018 as dataset
Setting clef2018 as dataset name
Selecting path ./results/ as result target
Selecting path ./jobs as job target
Repeating each method with 30 different seed sets
Executing jobs with Low memory requirements with 8 CPU cores
Executing jobs with Medium memory requirements wth 4 CPU cores
Executing jobs with High memory requirements with 1 CPU cores
```

## Reading the results

In the specified `results` directory (e.g., `./results/`), the raw
results of a run are stored. For each run, a PDF file and a Python
object containing the raw data that generated the plot are generated.
This object is stored in `pickle` form (file extension `.pkl`), which
can be read using the `pickle` library, which is included in the Python
standard library.

With the script `scripts/readdata.py`, the raw results of all run can be
aggregated in a single Pandas DataFrame. This script can be run as
follows:

``` console
$ python3 readdata.py -s ./path/to/results/synergy -t synergy.pkl
# OR
$ ./read_results_podman.sh ./path/to/results/synergy synergy.pkl
# OR
$ ./read_results_docker.sh ./path/to/results/synergy synergy.pkl
```

This script will read all the results stored in that specific directory
and generate a Pandas DataFrame. This file is stored as a pickle. This
can be read with the following code fragment.

``` python
import pandas as pd
pd.read_pickle("/path/to/pickle_file.pkl")
```

## Raw results

The raw results of our experiments can be downloaded using the following
links. They are archived as `tar.xz` files for each dataset.

- [CLEF2017](https://npai.science.uu.nl/clefdatasets/clef2017_results.tar.xz)
- [CLEF2018](https://npai.science.uu.nl/clefdatasets/clef2018_results.tar.xz)
- [CLEF2019](https://npai.science.uu.nl/clefdatasets/clef2019_results.tar.xz)
- [SYNERGY](https://npai.science.uu.nl/clefdatasets/synergy_results.tar.xz)

## Citation

If you want to cite this repository specifically, go to
[ZENODO](https://zenodo.org/doi/10.5281/zenodo.10887073). Otherwise,
please cite the paper.

TODO: Insert BIBTEX of Paper

## References

<div id="refs" class="references csl-bib-body" entry-spacing="0">

<div id="ref-bron_2024_108698682" class="csl-entry">

<span class="csl-left-margin">\[1\]
</span><span class="csl-right-inline">Michiel P. Bron. 2024. Python
package python-allib.
[10.5281/zenodo.10869848](https://doi.org/10.5281/zenodo.10869848)</span>

</div>

<div id="ref-debruin" class="csl-entry">

<span class="csl-left-margin">\[2\]
</span><span class="csl-right-inline">Jonathan de Bruin, Yongchao Ma,
Gerbrich Ferdinands, Jelle Teijema, and Rens van de Schoot. 2023.
SYNERGY - Open machine learning dataset on study selection in systematic
reviews. [10.34894/HE6NAQ](https://doi.org/10.34894/HE6NAQ)</span>

</div>

<div id="ref-li2020" class="csl-entry">

<span class="csl-left-margin">\[3\]
</span><span class="csl-right-inline">Dan Li and Evangelos Kanoulas.
2020. When to Stop Reviewing in Technology-Assisted Reviews: Sampling
from an Adaptive Distribution to Estimate Residual Relevant Documents.
*ACM Transactions on Information Systems* 38, 4: 1–36.
[10.1145/3411755](https://doi.org/10.1145/3411755)</span>

</div>

</div>
