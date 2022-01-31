import os
from utils import RestApi
from utils import Command


class App:
    def __init__(self):
        self._api = RestApi()

    def start(self):
        self._api.run(callback_func=self.on_call)

    def on_call(self, command, args):
        args_str = ''
        for key, val in args.items():
            args_str += f'{key} {val} '
        args_str = args_str.strip()

        if command == Command.CONVERT:
            os.system(f'python convert.py {args_str}')
        elif command == Command.GENERATE:
            os.system(f'python generate_model_config.py {args_str}')
        elif command == Command.TRAIN:
            os.system(f'python train.py {args_str}')
        elif command == Command.PREDICT:
            os.system(f'python predict.py {args_str}')


if __name__ == '__main__':
    App().start()
