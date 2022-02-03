FROM continuumio/miniconda3

COPY . .
SHELL ["/bin/bash", "--login", "-c"]

EXPOSE 8443
COPY pipeline.py .
ENTRYPOINT [ "python", "pipeline.py"]