FROM rocker/r-ubuntu:22.04
RUN apt install -y python3 python3-pip r-cran-tidyverse r-cran-rcapture
RUN pip3 install -g python-allib
RUN addgroup --system app \
    && adduser --system --ingroup app app
WORKDIR /home/app
COPY app .
RUN chown app:app -R /home/app
USER app
RUN pip install python-allib