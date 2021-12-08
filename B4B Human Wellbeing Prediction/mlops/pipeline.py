import shutil
import time
from datetime import datetime

import cloudpickle
import luigi
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from tpot import TPOTClassifier


def default_file_name():
    return datetime.today().strftime('%d-%m-%Y_%H:%M:%S')


class ProcessData(luigi.Task):
    file_path = luigi.Parameter(default='../dataset/dataset.csv')
    output_path = luigi.Parameter(default=f'exported_datasets/{default_file_name()}.csv')
    target_name = luigi.Parameter(default='acceptability_90')
    time = luigi.Parameter(default=time.time())

    def output(self):
        return luigi.LocalTarget(self.output_path)

    def run(self):
        df = pd.read_csv(self.file_path)

        df = shuffle(df)

        df.rename(columns={self.target_name: 'target'}, inplace=True)

        df['datetime'] = pd.to_datetime(df['datetime'])

        df['hour'] = df['datetime'].dt.hour
        df['minute'] = df['datetime'].dt.minute
        df['second'] = df['datetime'].dt.second

        columns = [
            'temperature',
            'mean_temp_day',
            'heatindex',
            'room',
            'relative_humidity',
            'light_sensor_one_wavelength',
            'light_sensor_two_wavelength',
            'number_occupants',
            'activity_occupants',
            'door_state',
            'hour',
            'minute',
            'second',
            'target',
        ]

        df[columns].to_csv(self.output_path)


class OptimizeModel(luigi.Task):
    file_path = luigi.Parameter(default=f'exported_datasets/{default_file_name()}.csv')
    output_path_pipeline = luigi.Parameter(default=f'exported_pipelines/{default_file_name()}.py')
    output_path_model = luigi.Parameter(default=f'exported_models/{default_file_name()}.pkl')
    scoring_function = luigi.Parameter(default=None)
    score_threshold = luigi.FloatParameter(default=99)
    time = luigi.Parameter(default=time.time())

    def requires(self):
        return [ProcessData()]

    def run(self):
        df = pd.read_csv(self.file_path)

        features = [
            'temperature',
            'mean_temp_day',
            'heatindex',
            'room',
            'relative_humidity',
            'light_sensor_one_wavelength',
            'light_sensor_two_wavelength',
            'number_occupants',
            'activity_occupants',
            'door_state',
            'hour',
            'minute',
            'second',
            'target',
        ]

        y = df['target']
        X = df[features]

        X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y.values, test_size=0.33)

        self.set_status_message('Optimizing model')
        pipeline_optimizer = TPOTClassifier(
            generations=5,
            scoring=self.scoring_function,
            n_jobs=-1,
            early_stop=3,
            verbosity=3
        )

        self.set_status_message('Fitting model')
        pipeline_optimizer.fit(X_train, y_train)

        self.set_status_message('Scoring model')
        score = pipeline_optimizer.score(X_test, y_test)

        self.set_status_message(f'Model score: {score}')

        if self.score_threshold < (score * 100):
            pipeline_optimizer.export(self.output_path_pipeline, data_file_path=self.file_path)

            with open(self.output_path_model, 'wb') as file:
                cloudpickle.dump(self, file)

            shutil.copy(self.output_path_model, '../api/model.pkl')


if __name__ == '__main__':
    luigi.build([OptimizeModel()])
