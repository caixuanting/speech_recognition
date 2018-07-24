# Author: caixuanting@gmail.com

import unittest as ut

import tensorflow as tf

from estimator import create_estimator


def train_input_fn():
    features = {}

    features['feature'] = tf.constant(
        [
            [
                [0, 0, 0],
                [0, 0, 0],
                [1, 1, 1],
                [1, 1, 1]
            ],
            [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [1, 1, 1]
            ],
            [
                [1, 1, 1],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
            ],
            [
                [1, 1, 1],
                [1, 1, 1],
                [1, 1, 1],
                [0, 0, 0]
            ]
        ],
        dtype=tf.float32
    )

    features['sequence_length'] = [4, 4, 4, 4]

    labels = tf.SparseTensor(
        indices=[
            [0, 0], [0, 1],
            [1, 0], [1, 1],
            [2, 0], [2, 1],
            [3, 0], [3, 1]
        ],
        values=[
            0, 1,
            0, 1,
            1, 0,
            1, 0
        ],
        dense_shape=[4, 2]
    )

    return features, labels


def predict_input_fn():
    features = {}

    features['feature'] = tf.constant(
        [
            [
                [0, 0, 0],
                [1, 1, 1]
            ],
            [
                [1, 1, 1],
                [0, 0, 0]
            ]
        ],
        dtype=tf.float32
    )

    features['sequence_length'] = [2, 2]

    return features, None


class TestCreateEstimator(ut.TestCase):
    def test_create_estimator(self):
        params = {
            'model_type': 'lstm',
            'num_layers': 1,
            'num_units': 10,
            'num_classes': 3,
            'learning_rate': 0.01
        }

        estimator = create_estimator(params)

        tf.logging.set_verbosity(tf.logging.INFO)

        estimator.train(input_fn=train_input_fn, steps=10000)

        predictions = estimator.predict(input_fn=predict_input_fn)

        softmax = None

        count = 0

        for key, value in enumerate(predictions):
            if count == 2:
                break

            softmax = value['softmax']
            print(softmax)
            count = count + 1


if __name__ == '__main__':
    ut.main()
