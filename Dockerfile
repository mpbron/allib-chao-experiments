FROM rocker/r-ubuntu:22.04 as builder
ENV PYTHONUNBUFFERED 1

RUN apt update
RUN apt install -y python3 python3-pip python3-venv
RUN python3 -m venv /opt/venv

# Enable venv
ENV PATH="/opt/venv/bin:$PATH"
COPY ./requirements.txt /app/requirements.txt
RUN pip install -Ur /app/requirements.txt


FROM rocker/r-ubuntu:22.04 as runner
RUN apt update
RUN apt install -y python3 python3-pip python3-venv
RUN apt install -y r-cran-tidyverse r-cran-rcapture parallel
COPY --from=builder /opt/venv /opt/venv

# Enable venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app/
COPY scripts/ .
RUN chmod +x *.sh
RUN mkdir parameters output
CMD ["/bin/bash"]