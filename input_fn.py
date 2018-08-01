# Author: caixuanting@gmail.com

import tensorflow as tf

from constant import FEATURE
from constant import LABEL
from constant import LENGTH


def _pad_features(features, max_length):
    """
    Pad features to the same length
    Use the last element of each sequence to pad itself

    Input:
        features - feature sequences
        max_length - max length of feature sequences

    Output:
        padded_features - feature sequences with the same length
    """

    padded_features = []

    for feature in features:
        feature_length = len(feature)

        if feature_length < max_length:
            padded_values = [feature[-1]] * (max_length - feature_length)
            feature = feature + padded_values
        padded_features.append(feature)

    return padded_features


def _parse_from_proto(string_examples):
    """
    Generate label, length and feature list from SequenceExample proto.

    Input:
        string_examples - SequenceExample in serialized string format

    Output:
        labels - batch of labels in list format
        lengths - batch of lengths in list format
        features - batch of features in list format
    """

    labels, lengths, features = [], [], []

    for string_example in string_examples:
        proto_example = tf.train.SequenceExample()
        proto_example.ParseFromString(string_example)

        context = proto_example.context

        labels.append(list(context.feature[LABEL].int64_list.value))
        lengths = lengths + map(int, context.feature[LENGTH].int64_list.value)

        feature = [f.float_list.value for f in proto_example.feature_lists.feature_list[FEATURE].feature]

        features.append(feature)

    return labels, lengths, features


def _parse_example(string_examples):
    """
    Parse tf.record into tensor format

    Input:
        string_examples - batch of tf.examples in serialized string format

    Output:
        indices - indices for label sparse tensor
        values - values for label sparse tensor
        dense_shape - dense shape for label sparse tensor
        lengths - lengths of feature sequences
        padded_features - padded feature sequences, padded with last element of each sequence
    """

    labels, lengths, features = _parse_from_proto(string_examples)

    max_length = max(lengths)

    padded_features = _pad_features(features, max_length)

    indices, values = [], []

    dense_shape = [len(labels), max([len(x) for x in labels])]

    for i in range(len(labels)):
        values = values + map(int, labels[i])

        for j in range(len(labels[i])):
            indices.append([i, j])

    return indices, values, dense_shape, lengths, padded_features


def train_input_fn(filenames, num_features, buffer_size, batch_size, num_epochs):
    """
    Generate feature and label batch.

    Input:
        filenames - a list of files containing tfrecord
        num_features - number of features for each frame
        buffer_size - buffer size for reshuffle queue
        batch_size - number of examples for each batch
        num_epochs - number of times to go through examples

    Output:
        features - a dictionary contains sequence length and sequence feature
        labels - sequence label
    """

    dataset = tf.data.TFRecordDataset(filenames)

    dataset = dataset.shuffle(buffer_size=buffer_size)
    dataset = dataset.batch(batch_size=batch_size)
    dataset = dataset.repeat(count=num_epochs)

    dataset = dataset.map(lambda x: tf.py_func(
        func=_parse_example,
        inp=[x],
        Tout=([tf.int64, tf.int64, tf.int64, tf.int64, tf.float64])))

    iterator = dataset.make_one_shot_iterator()

    indices, values, dense_shape, lengths, padded_features = iterator.get_next()

    values = tf.cast(values, dtype=tf.int32)
    labels = tf.SparseTensor(indices=indices, values=values, dense_shape=dense_shape)

    padded_features.set_shape([batch_size, None, num_features])
    padded_features = tf.cast(padded_features, dtype=tf.float32)
    features = {
        FEATURE: padded_features,
        LENGTH: lengths
    }

    return features, labels


def eval_input_fn():
    """
    Generate evaluation example

    Output:
        features - a dictionary contains length and feature
        labels - None
    """

    dataset = tf.data.Dataset.from_tensor_slices({
        FEATURE: tf.constant(
            [
                [
                    [0],
                    [1],
                    [2]
                ],
                [
                    [2],
                    [1],
                    [0]
                ],
                [
                    [1],
                    [1],
                    [2]
                ],
                [
                    [2],
                    [0],
                    [1]
                ]
            ],
            dtype=tf.float32),
        LENGTH: [3, 3, 3, 3]
    })

    dataset = dataset.batch(batch_size=1)

    iterator = dataset.make_one_shot_iterator()

    return iterator.get_next(), None
