import os
from collections import ChainMap
from configparser import ConfigParser
from datetime import datetime
from pathlib import Path


def read_configs(path, loaded_models) -> []:
    parser = ConfigParser()
    configs = []

    for cfg in os.listdir(path):
        parser.read(path / cfg)
        config = {
            'model': parser.get('model', 'name'),
            'targets': eval(parser.get('data', 'targets')),
            'groups': eval(parser.get('data', 'groups')),
            'unreels': eval(parser.get('data', 'unknown-reels')),
            'uncats': eval(parser.get('data', 'unknown-categoricals')),
            'knreels': eval(parser.get('data', 'known-reels')),
            'kncats': eval(parser.get('data', 'known-categoricals')),
            'batch': eval(parser.get('training', 'batch-size')),
            'learning-rate': eval(parser.get('training', 'learning-rate')),
            'hyper-tuning': parser.has_section('hyper-tuning')
        }

        for model in loaded_models:
            if config['model'] == model.name:
                config = dict(ChainMap(config, model.read_metadata(parser, **{'hyper-tuning': config['hyper-tuning']})))

        configs.append(config)

    return configs


def write_config(model, **kwargs):
    main_config = read_main_config()

    configparser = ConfigParser()
    configparser.add_section('model')
    configparser.set(section='model', option="name", value=model.name)

    configparser.add_section('data')
    configparser.set(section='data', option='groups', value=str([]))
    configparser.set(section='data', option='targets', value=str([]))
    configparser.set(section='data', option='unknown-categoricals', value=str([]))
    configparser.set(section='data', option='unknown-reels', value=str([]))
    configparser.set(section='data', option='known-categoricals', value=str([]))
    configparser.set(section='data', option='known-reels', value=str([]))

    configparser.add_section('training')
    configparser.set(section='training', option='batch-size', value=str(128))
    configparser.set(section='training', option='learning-rate', value=str(0.01))

    model.generate_config(configparser, **kwargs)

    with open(Path(main_config['model-configs']) / f'model_{model.name}.cfg', 'w') as configfile:
        configparser.write(configfile)


def export_metadata(model, df, pl):
    """
    Generation of metadata file for the models

    :param df: dataframe from dataset
    :param config: configuration on which the model is trained
    :param model: model
    :param pl: saving_path
    :return: [model_name, id, data_source, targets, column_name]
    """
    configparser = ConfigParser()
    configparser.add_section('model')
    configparser.set(section='model', option="name", value=model.metadata['model'])
    configparser.set(section='model', option="id", value=str(model.model_id))

    configparser.add_section('data')
    configparser.set(section='data', option='columns', value=str(list(df.columns.values)))
    configparser.set(section='data', option='groups', value=str(model.metadata['groups']))
    configparser.set(section='data', option='targets', value=str(model.metadata['targets']))
    configparser.set(section='data', option='unknown-categoricals', value=str(model.metadata['uncats']))
    configparser.set(section='data', option='unknown-reels', value=str(model.metadata['unreels']))
    configparser.set(section='data', option='known-categoricals', value=str(model.metadata['kncats']))
    configparser.set(section='data', option='known-reels', value=str(model.metadata['knreels']))

    configparser.add_section('training')
    configparser.set(section='training', option='batch-size', value=str(model.metadata['batch']))
    configparser.set(section='training', option='learning-rate', value=str(model.metadata['learning-rate']))

    model.write_metadata(configparser)

    path = str((pl / f'metadata-{datetime.now().strftime("%H%M%S")}-{model.model_id}.cfg').absolute())
    with open(path, 'w') as configfile:
        configparser.write(configfile)


def read_metadata(file, loaded_models, **kwargs) -> {}:
    """
   Reads the metadata file that was generated when the model was trained

   :param file: location of the file
   :param loaded_models: list of models that has been loaded in script
   :return: [model_name, model_id, data_source, targets, column_names]
   """
    configparser = ConfigParser()
    configparser.read(file)

    config = {
        'model': configparser.get('model', 'name'),
        'id': configparser.get('model', 'id'),
        'columns': eval(configparser.get('data', 'columns')),
        'groups': eval(configparser.get('data', 'groups')),
        'targets': eval(configparser.get('data', 'targets')),
        'uncats': eval(configparser.get('data', 'unknown-categoricals')),
        'unreels': eval(configparser.get('data', 'unknown-reels')),
        'kncats': eval(configparser.get('data', 'known-categoricals')),
        'knreels': eval(configparser.get('data', 'known-reels')),
        'batch': eval(configparser.get('training', 'batch-size')),
        'learning-rate': eval(configparser.get('training', 'learning-rate')),
        'hyper-tuning': configparser.has_section('hyper-tuning')
    }

    for model in loaded_models:
        config = dict(ChainMap(config, model.read_metadata(configparser, **{'hyper-tuning': config['hyper-tuning']})))

    return config


def read_main_config():
    configparser = ConfigParser()
    configparser.read(Path(__file__).parent.parent.absolute() / 'config.cfg')

    config = {
        'wandb': str(configparser.get(section='wandb', option='wandb')).lower() == 'true',
        'wandb-key': configparser.get(section='wandb', option='wandb-key'),
        'wandb-project': configparser.get(section='wandb', option='wandb-project'),
        'wandb-team': configparser.get(section='wandb', option='wandb-team'),
        'output-path-data': configparser.get(section='output', option='output-path-data'),
        'output-path-model': configparser.get(section='output', option='output-path-model'),
        'output-path-reports': configparser.get(section='output', option='output-path-reports'),
        'output-path-predictions': configparser.get(section='output', option='output-path-predictions'),
        'model-configs': configparser.get(section='input', option='input-model-configs')
    }

    _create_dirs_if_not_exists(
        paths=[
            config['output-path-data'],
            config['output-path-model'],
            config['output-path-reports'],
            config['output-path-predictions']
        ]
    )

    return config


def _create_dirs_if_not_exists(paths):
    for path in paths:
        final_path = str((Path(__file__).parent.parent / path).absolute())

        if not os.path.isdir(final_path):
            os.makedirs(final_path)
