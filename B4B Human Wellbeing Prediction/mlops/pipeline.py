import glob
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
    return datetime.today().strftime('%d-%m-%Y_%H-%M-%S')


class CombineData(luigi.Task):
    folder_path = luigi.Parameter(default='../datasets/*.csv')
    time = luigi.Parameter(default=time.time())
    output_path = f'combined_datasets/{default_file_name()}.csv'

    def output(self):
        return luigi.LocalTarget(self.output_path)

    def run(self):
        files = glob.glob(self.folder_path)

        csv = pd.concat([pd.read_csv(file) for file in files])

        csv.to_csv(self.output_path, index=False)


class ProcessData(luigi.Task):
    target_name = luigi.Parameter(default='acceptability_90')
    time = luigi.Parameter(default=time.time())
    output_path = f'processed_datasets/{default_file_name()}.csv'

    def requires(self):
        return [CombineData()]

    def output(self):
        return luigi.LocalTarget(self.output_path)

    def run(self):
        file_path = self.input()[0].path

        df = pd.read_csv(file_path)

        df = shuffle(df)

        df.rename(columns={self.target_name: 'target'}, inplace=True)

        df = pd.get_dummies(df, columns=['room'])

        drop = [
            'original_entry_id',
            'node_id',
            'datetime',
            'acceptability_80',
            'tmp_cmf',
            'tmp_cmf_80_low',
            'tmp_cmf_80_up',
            'tmp_cmf_90_low',
            'tmp_cmf_90_up',
        ]

        df = df.drop(drop, axis=1)
        df.to_csv(self.output_path)


class OptimizeModel(luigi.Task):
    generations = luigi.Parameter(default=10)
    scoring_function = luigi.Parameter(default=None)
    score_threshold = luigi.FloatParameter(default=99)
    tpot_config = luigi.Parameter(default='TPOT NN')
    time = luigi.Parameter(default=time.time())
    output_file = f'exported_models/{default_file_name()}.pkl'

    def requires(self):
        return [ProcessData()]

    def run(self):
        file_path = self.input()[0].path

        df = pd.read_csv(file_path)

        y = df['target']
        X = df.drop('target', axis=1)

        X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y.values, test_size=0.33)

        self.set_status_message('Optimizing model')
        pipeline_optimizer = TPOTClassifier(
            generations=self.generations,
            scoring=self.scoring_function,
            n_jobs=-1,
            max_eval_time_mins=10,
            config_dict=self.tpot_config,
            periodic_checkpoint_folder=f'tpot_logs/{default_file_name()}',
            early_stop=3,
            verbosity=3,
            log_file=f'tpot_logs/{default_file_name()}.txt',
        )

        self.set_status_message('Fitting model')
        pipeline_optimizer.fit(X_train, y_train)

        self.set_status_message('Scoring model')
        score = pipeline_optimizer.score(X_test, y_test)

        self.set_status_message(f'Model score: {score}')

        if self.score_threshold < (score * 100):
            pipeline_optimizer.export(f'exported_pipelines/{default_file_name()}.py', data_file_path=file_path)

            with open(self.output_file, 'wb') as file:
                cloudpickle.dump(self, file)

            shutil.copy(self.output_file, '../api/model.pkl')


if __name__ == '__main__':
    luigi.build([OptimizeModel()])
