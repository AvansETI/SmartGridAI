"""
A training file that can take multiple models, train them and evaluate them.

Command-arguments:
    -d [--DATA]: Data file path, must be a .csv file.
    -m [--MODEL]: Model file paths, must be a file. If specified it will continue training that model.
    -e [--EPOCHS]: The amount of epochs the model needs to be trained
    -tr [--TRIALS]: The amount of trials the hyper-tuning must execute
"""

import importlib
import inspect
import os
import uuid
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd

import wandb
from utils import config_reader

model_classes = []
main_config = config_reader.read_main_config()


def parse_args():
    """
    Parse the arguments from the command using argparse

    :return: argument-parser
    """
    parser = ArgumentParser(add_help=True)

    parser.add_argument(
        '-d', '--data',
        required=True,
        type=str,
        help='Data file path, must be a .csv file in the out/datasets directory.'
    )

    parser.add_argument(
        '-m', '--model',
        action='extend',
        nargs='*',
        default=[],
        help='Model file paths, must be a (.?) file. If specified this model will be trained'
    )

    parser.add_argument(
        '-e', '--epochs',
        default=100,
        type=int,
        help='Amount of epochs to training. Default: 100'
    )

    parser.add_argument(
        '-tr', '--trials',
        default=100,
        type=int,
        help='Trials should only be used whenever hypertuning is activated. Trials specifies the amount of trials it '
             'will maximally run before coming to the best results. Default: 100 '
    )

    return parser.parse_args()


def find_model(name):
    """
    Finds the model based on name. If none exists it will return None

    :param name: model_name
    :return: model
    """
    for model in model_classes:
        if str(model.name) == str(name):
            return model


def check_compatability(df, columns):
    """
    Checks whether or not the model is can be used to predict a forecast based on the data that was provided

    :param df: Dataframe that is loaded in for predicting or training
    :param columns: columns in the metadata that was generated for model
    :return: Boolean, [missing_columns]
    """
    df_columns = list(df.columns.values)

    missing_columns = []

    compatability = True

    for column in columns:
        if not df_columns.__contains__(column):
            missing_columns.append(column)
            compatability = False

    return compatability, missing_columns


def main(args):
    """
    The main method that runs whenever the file is being used.

    :param args: the arguments in the command.

    This method loops through the chosen models and executes

    Model.generate_time_series_dataset

    if hypertuning is enabled it will call:

        -Model.tune_hyper_parameter

    else it will check for an existing model otherwise it will generate a new model.
        -Model.load_model
        -Model.generate_model

    -Model.train_model
    -Model.evaluate_model

    :return: Nothing
    """

    global metadata, weights_file

    if main_config['wandb']:
        print('Using WandB')
        if main_config['wandb-key'] is not None and main_config['wandb-team'] is not None and main_config['wandb-project'] is not None:
            os.environ['WANDB_API_KEY'] = main_config['wandb-key']

            wandb.init(project=main_config['wandb-project'], entity=main_config['wandb-team'])
            wandb.login()
            print('Successfully logged in WandB')
        else:
            print('Incorrect WandB credentials')
    else:
        print('Not using WandB')

    df_path = str((Path(__file__).parent / main_config['output-path-data'] / args.data).absolute())
    df = pd.read_csv(df_path, parse_dates=['Timestamp'])

    if len(args.model) != 0:

        created_models = []
        files = []

        for model_id in args.model:
            p = (Path(__file__).parent / main_config['output-path-model']).absolute()

            for model_type in os.listdir(p):
                p_type = p / model_type
                for model_id_ in os.listdir(p_type):
                    if model_id == model_id_:
                        # Found correct directory
                        p = p / model_type / model_id / 'checkpoints'
                        break
                else:
                    continue
                break

            for file in os.listdir(p):
                if file.endswith('.cfg') & file.startswith('metadata'):
                    metadata = config_reader.read_metadata(p / file, loaded_models=model_classes)
                else:
                    weights_file = p / file

            if metadata is not None:
                model = find_model(metadata['model'])

                if model is None:
                    print(f"Couldn't find model: {metadata['model']}")
                    quit(101)
                    break

                model_class = model(metadata, df)

                compatability, missing_columns = check_compatability(df, metadata['columns'])

                if not compatability:
                    print(
                        'One of the models is not compatible with the dataset and is missing: ' + str(missing_columns))
                    quit(102)
                    break

                if weights_file is None:
                    print(f'Cannot find weights-file for model: {metadata["id"]}')
                    quit(104)
                    break

                created_models.append(model_class)
                files.append(weights_file)
            else:
                print(f"Cannot load in metadata. Directory: {model_id}")
                quit(103)
                break

        for index in range(0, len(created_models)):
            model = created_models[index]
            file = files[index]

            training = model.generate_time_series_dataset()

            trained_model = model.load_model(file)

            os.remove(file)

            trained_model = model.train_model(trained_model, training, **vars(args))

            model.evaluate_model(trained_model, training)

    else:
        configs = config_reader.read_configs(Path(main_config['model-configs']).absolute(), loaded_models=model_classes)

        for config in configs:
            model = find_model(config['model'])

            if model is not None:
                model_id = uuid.uuid4()

                config['id'] = model_id

                model_class = model(config, df)

                training = model_class.generate_time_series_dataset()

                if config['hyper-tuning']:
                    trained_model = model_class.tune_hyper_parameter(training, **vars(args))
                else:
                    c_model = model_class.generate_model(training)

                    trained_model = model_class.train_model(c_model, training, **vars(args))

                metadata_export_path = Path(main_config['output-path-model']) / f'{model_class.name}' / f'{model_id}'

                # Model output changes when WandB is enabled as logger
                if (main_config['wandb']) and (main_config['wandb-project'] is not None):
                    id_generated_dir = os.listdir(metadata_export_path / str(main_config['wandb-project']))[0]
                    metadata_export_path = (metadata_export_path / str(main_config['wandb-project']) / id_generated_dir / 'checkpoints')
                else:
                    metadata_export_path = (metadata_export_path / 'checkpoints')

                config_reader.export_metadata(model_class, df, metadata_export_path)

                try:
                    model_class.evaluate_model(trained_model, training)
                except:
                    print("Could not evaluate model, check if evaluate_model can be loaded in and predict correctly.")

            else:
                print(f"Couldn't find model: {config['model']}")
                quit(102)
                break


if __name__ == '__main__':
    # search models in folder
    c = importlib.import_module('models')

    for name_local in dir(c):
        if inspect.isclass(getattr(c, name_local)):
            Model = getattr(c, name_local)
            model_classes.append(Model)
            print(f"{Model.name} model has been loaded in")

    main(parse_args())
