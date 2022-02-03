FROM continuumio/miniconda3

COPY . .
SHELL ["/bin/bash", "--login", "-c"]

COPY env.yml .
RUN conda env create -f env.yml
RUN conda init bash
RUN echo "conda activate b4b_env" >> ~/.bashrc

EXPOSE 5000
#RUN echo "python app.py" >> ~/.bashrc
COPY app.py .
ENTRYPOINT ["conda", "run", "-n", "b4b_env", "python", "app.py"]