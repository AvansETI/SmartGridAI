"""
This package is used for implementing different kind of models into the train.py & predict.py and

To create a model it must suffice to the primary methods defined in model.py

Example:

class ExampleModel(ABC, Model):

    name = 'Name of the model that will be used in the command'

    read_metadata = lambda configparser, **kwargs: read_metadata(configparser, **kwargs)
    generate_config = lambda configparser, **kwargs: generate_config(configparser, **kwargs)

    def __init__(self, model_id, data):
        super().__init__(model_id, data)

    def generate_time_series_dataset(self, **kwargs):
        #your code

    def generate_model(self, dataset, **kwargs):
        #your code

    def load_model(self, **kwargs):
        #your code

    def train_model(self, dataset, created_model, **kwargs):
        #your code

     def predict(self, model, **kwargs):
        #your code

    def tune_hyper_parameter(self, dataset, **kwargs):
        #your code

    def evaluate_model(self, model, dataset, **kwargs):
        #your code

    def write_metadata(configparser)
        #your code

def read_metadata(configparser, **kwargs):
    #your code

def generate_config(configparser, **kwargs):
    #your code

"""

from models.tft_model import Tft
