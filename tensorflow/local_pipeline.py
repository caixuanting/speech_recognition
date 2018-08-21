# Author: caixuanting@gmail.com

import tensorflow as tf

from constant import SOFTMAX
from estimator import create_estimator
from input_fn import eval_input_fn
from input_fn import train_input_fn
from parser import create_params
from parser import parse


def main(argv):
    param_namespace = parse(argv[1:])

    params = create_params(param_namespace)

    estimator = create_estimator(params)

    tf.logging.set_verbosity(tf.logging.INFO)

    estimator.train(
        input_fn=lambda: train_input_fn(
            param_namespace.filenames,
            param_namespace.num_features,
            param_namespace.buffer_size,
            param_namespace.batch_size,
            param_namespace.num_epochs
        ),
        steps=param_namespace.steps)

    predictions = estimator.predict(input_fn=eval_input_fn)

    for key, value in enumerate(predictions):
        print('------------------key:', key)
        for row in value[SOFTMAX]:
            row = list(row)
            print('max index: %1d' % row.index(max(row)))


if __name__ == '__main__':
    tf.app.run()
