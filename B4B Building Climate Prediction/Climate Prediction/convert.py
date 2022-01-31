"""
A convert file that converts the existing dataset to a dataset that the other script can use.

Command-arguments:
    -d [--DATA]: Data filepath, must be a .csv file.
    -t [--TIMESTAMP]: The column which contains the timestamps
    -r [--RESAMPLE]: Resample the duration. Default: Min For all options see: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.resample.html
    -n [--NAME]: Name of the exported file
"""

import uuid
import pandas as pd
from pathlib import Path
from argparse import ArgumentParser
from utils import config_reader

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
        help='Data file path, must be a .csv file.'
    )

    parser.add_argument(
        '-t', '--timestamp',
        required=True,
        type=str,
        help='Feature column which included the timestamp.'
    )

    parser.add_argument(
        '-r', '--resample',
        default='min',
        type=str,
        help='Resample duration. Default: min. For all options see: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.resample.html'
    )

    parser.add_argument(
        '-n', '--name',
        type=str,
        help='Name of exported file'
    )

    return parser.parse_args()


def main(args):
    """
    The main method that runs whenever the file is being used.

    :param args: the arguments in the command

    It resamples the timestamps and generates indexes.

    Generates a new csv file with the applied transformations.

    :return: nothing
    """
    df = pd.read_csv(args.data, parse_dates=['Timestamp'])

    if 'Timestamp' not in df.columns:
        df['Timestamp'] = df[args.timestamp]
        del df[args.timestamp]

    df.sort_values(by='Timestamp', inplace=True)
    df = df.resample(args.resample, on='Timestamp').median()
    df = df.reset_index()
    df.dropna(inplace=True)
    df['Index'] = df.index

    name = args.name
    if name is None:
        name = f'dataset-{uuid.uuid4()}'

    path = str((Path(__file__).parent / main_config['output-path-data'] / f'{name}.csv').absolute())
    df.to_csv(path, index=False)


if __name__ == '__main__':
    main(parse_args())
