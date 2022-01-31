from typing import Any, Dict


class Model:
    """
    Base class for the models.
    """

    def __init__(self, metadata, data):
        self.data = data
        self.metadata = metadata
        self.model_id = metadata['id']

    def generate_time_series_dataset(self) -> Any:
        """
        Generate a dataset that contains time-series dataset. This is not 100% necessary since not all models
        need a specialized timeseries dataset from PyTorch’s library. Feel free to use this method to convert or
        clean up the data.

        This method should still be implemented though. You should just return the dataset in case you don't really
        need this method.

        :return: a time-series dataset
        """
        raise NotImplementedError()

    def generate_model(self, data) -> Any:
        """
        Generate a model that can take a time-series dataset in as training.
        It is possible that your model doesn't need the dataset to generate. In that case the data parameter
        can just be ignored.

        :param data: a time-series dataset

        :return: an untrained model
        """
        raise NotImplementedError()

    def train_model(self, model, dataset, **kwargs) -> Any:
        """
        Train model that has been generated.

        :param model: the untrained model
        :param dataset: the dataset from generate_time_series_dataset

        :return: a trained model
        """
        raise NotImplementedError()

    def load_model(self, path, **kwargs) -> Any:
        """
        Load in a pre-trained model from files that has been generated by this algorithm

        :return: a trained model
        """
        raise NotImplementedError()

    def predict(self, model, **kwargs) -> Dict:
        """
        Predict an amount of time steps into the future by using the pre-trained model

        :param model: a trained model

        :return: a dictionary of predictions per target feature
        """
        raise NotImplementedError()

    def tune_hyper_parameter(self, dataset, **kwargs) -> Any:
        """
        Hyper tune the model. Implementations should both save the best model into the output-path-model directory as
        return it.
        It is normal that this method is CPU/GPU intensive and that it takes a lot of time.

        :param dataset: A timeseries dataset

        :return: the best hyper-tuned model
        """
        raise NotImplementedError()

    def evaluate_model(self, evaluated_model, dataset):
        """
        Train model that has been generated. Some sort of report can be generated with this method.

        :param evaluated_model: the model to be evaluated
        :param dataset: the dataset from generate_time_series_dataset

        :return: nothing
        """

        raise NotImplementedError()

    def write_metadata(self, configparser):
        """
        Writes the metadata from a model (This is per model very different based on what data it needs)

        :param configparser: ConfigParser

        :return: Nothing
        """
        raise NotImplementedError()
