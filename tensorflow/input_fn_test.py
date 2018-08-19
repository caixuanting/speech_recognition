# Author: caixuanting@gmail.com

import unittest as ut

import tensorflow as tf

from constant import FEATURE
from constant import LENGTH
from input_fn import eval_input_fn
from input_fn import train_input_fn


class TestInputFnMethods(ut.TestCase):
    def test_train_input_fn_single(self):
        features, labels = train_input_fn(['test_data/input_fn_test.tfrecord'],
                                          1,  # num_features
                                          1,  # buffer_size
                                          1,  # batch_size
                                          1,  # num_epochs
                                          )

        session = tf.Session()

        result_features, result_labels = session.run([features, labels])

        length = result_features[LENGTH]
        self.assertEqual(8, length)

        feature = result_features[FEATURE]
        self.assertListEqual([1., 0., 1., 2., 1., 2., 2., 1.], list(feature.flatten()))

        self.assertListEqual([0, 0,
                              0, 1,
                              0, 2,
                              0, 3,
                              0, 4,
                              0, 5,
                              0, 6],
                             list(result_labels.indices.flatten()))

        self.assertListEqual([1, 0, 1, 2, 1, 2, 1], list(result_labels.values))

        self.assertListEqual([1, 7], list(result_labels.dense_shape))

    def test_train_input_fn_batch(self):
        features, labels = train_input_fn(['test_data/input_fn_test.tfrecord'],
                                          1,  # num_features
                                          5,  # buffer_size
                                          2,  # batch_size
                                          1,  # num_epochs
                                          )

        session = tf.Session()

        result_features, result_labels = session.run([features, labels])

        length = result_features[LENGTH]
        self.assertEqual(2, len(length))

        feature = result_features[FEATURE]
        self.assertEqual(2, len(feature))
        self.assertEqual(max(length), len(feature[0]))
        self.assertEqual(max(length), len(feature[1]))

        self.assertEqual(len(result_labels.values), len(result_labels.indices))
        self.assertEqual(2, len(result_labels.dense_shape))

    def test_eval_input_fn(self):
        features, _ = eval_input_fn()

        session = tf.Session()

        result_features = session.run([features])[0]

        length = result_features[LENGTH]
        self.assertEqual(3, length)

        feature = result_features[FEATURE]
        self.assertListEqual([0, 1, 2], list(feature.flatten()))


if __name__ == '__main__':
    ut.main()
