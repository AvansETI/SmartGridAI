import glob
import shutil
import time

import cloudpickle
import luigi
import pandas as pd
import shap
from sklearn.metrics import make_scorer
from sklearn.utils import shuffle
from tpot import TPOTClassifier

from helpers import get_data_and_split, custom_scoring, default_file_name


class CombineData(luigi.Task):
    folder_path = luigi.Parameter(default='../datasets/*.csv')
    time = luigi.Parameter(default=time.time())
    output_path = f'combined_datasets/{default_file_name()}.csv'

    def output(self):
        return luigi.LocalTarget(self.output_path)

    def run(self):
        files = glob.glob(self.folder_path)

        csv = pd.concat([pd.read_csv(file, index_col=[0]) for file in files])

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
        df.to_csv(self.output_path, index=False)


class OptimizeModel(luigi.Task):
    generations = luigi.Parameter(default=10)
    scoring_function = luigi.Parameter(default=None)
    time = luigi.Parameter(default=time.time())
    output_file = f'exported_models/{default_file_name()}.pkl'

    def requires(self):
        return [ProcessData()]

    def output(self):
        return luigi.LocalTarget(self.output_file)

    def run(self):
        file_path = self.input()[0].path
        X_train, X_test, y_train, y_test = get_data_and_split(file_path)

        if self.scoring_function is None:
            self.scoring_function = make_scorer(custom_scoring, greater_is_better=True)

        pipeline_optimizer = TPOTClassifier(
            generations=5,
            population_size=10,
            scoring=self.scoring_function,
            n_jobs=-1,
            max_eval_time_mins=10,
            periodic_checkpoint_folder=f'tpot_logs/{default_file_name()}',
            early_stop=3,
            verbosity=3,
            log_file=f'tpot_logs/{default_file_name()}.txt',
        )

        pipeline_optimizer.fit(X_train, y_train)

        pipeline_optimizer.export(f'exported_pipelines/{default_file_name()}.py', data_file_path=file_path)

        with open(self.output_file, 'wb') as file:
            cloudpickle.dump(pipeline_optimizer.fitted_pipeline_, file)


class DeployModel(luigi.Task):
    score_threshold = luigi.FloatParameter(default=0.99 * 9)
    time = luigi.Parameter(default=time.time())

    def requires(self):
        return [ProcessData(), OptimizeModel()]

    def run(self):
        data_file_path = self.input()[0].path
        X_train, X_test, y_train, y_test = get_data_and_split(data_file_path)

        model_file_path = self.input()[1].path
        with open(model_file_path, "rb") as file:
            model = cloudpickle.load(file)

        score = model.score(X_test, y_test)

        print(self.score_threshold)
        print(score)

        if self.score_threshold < score:
            shutil.copy(model_file_path, '../api/model.pkl')


class DeployShap(luigi.Task):
    score_threshold = luigi.FloatParameter(default=0.99 * 9)
    time = luigi.Parameter(default=time.time())

    def requires(self):
        return [ProcessData(), OptimizeModel()]

    def run(self):
        data_file_path = self.input()[0].path
        X_train, X_test, y_train, y_test = get_data_and_split(data_file_path)

        model_file_path = self.input()[1].path
        with open(model_file_path, "rb") as file:
            pipeline = cloudpickle.load(file)

        score = pipeline.score(X_test, y_test)

        print(self.score_threshold)
        print(score)

        if self.score_threshold < score:
            explainer = shap.KernelExplainer(pipeline.predict_proba, shap.kmeans(X_train, 15))
            with open('../api/explainer.pkl', 'wb') as file:
                cloudpickle.dump(explainer, file)


if __name__ == '__main__':
    luigi.build([DeployModel(), DeployShap()])
