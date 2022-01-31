# Brains4Buildings Climate Prediction
"A framework to predict the inside climate of buildings"

## Dependencies
- `Anaconda`, to easily create a Python environment

Make sure all dependencies work in PowerShell/Terminal before continuing.

## Setup
1. Create conda environment with: `conda create -n [name] python=3.8`
2. Activate environment with: `conda activate [name]`
3. Install requirements with: `pip install -r requirements.txt`

## Usage
RTFM. For examples see this [Colab Notebook](https://colab.research.google.com/drive/17hVvRTiqt9mxTbp2X3z7_KNIE76FbVZc?usp=sharing).

## Docker
You can use this project within a Docker container. Make sure to have the latest version of Docker installed and spin up the container with `docker-compose up -d`. The application will listen to HTTP-requests (examples can be found in the /http directory) on port 8081.
