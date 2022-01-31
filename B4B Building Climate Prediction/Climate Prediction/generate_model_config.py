"""
A script that generates config files for the models.
The generated config files will be stored in the 'configs' folder.

Command-arguments:
    [MODEL_NAMES]
    -hy [--HYPER]: If it needs to be hyper-tuned
"""

import importlib
import inspect
from argparse import ArgumentParser
from pathlib import Path

from utils import config_reader

model_classes = []


def parse_args():
    """
    Parse the arguments from the command using argparse

    :return: argument-parser
    """
    parser = ArgumentParser(add_help=True)

    parser.add_argument(
        '-hy', '--hyper',
        action='store_true',
        help='specifies if this model is meant to be hyper-tuned'
    )

    for model in model_classes:
        parser.add_argument(model.name)

    return parser.parse_args()


def main(args):
    for model in model_classes:
        if vars(args)[model.name] is not None:
            config_reader.write_config(model, **vars(args))


if __name__ == '__main__':
    # search models in folder
    package_dir = Path(__file__).parent / 'models'

    c = importlib.import_module(f"{package_dir}")

    for name_local in dir(c):
        if inspect.isclass(getattr(c, name_local)):
            Model = getattr(c, name_local)
            model_classes.append(Model)
            print(f"{Model.name} model has been loaded in")

    main(parse_args())
