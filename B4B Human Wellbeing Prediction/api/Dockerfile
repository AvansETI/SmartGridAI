FROM continuumio/miniconda3

COPY . .
SHELL ["/bin/bash", "--login", "-c"]

COPY env.yml .
RUN conda env create -f env.yml
RUN conda init bash

EXPOSE 5000
COPY app.py .
ENTRYPOINT ["conda", "run", "-n", "b4b_env", "python", "app.py"]