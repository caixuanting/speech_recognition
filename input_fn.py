# coding=utf-8
# Author: caixuanting@gmail.com

import tensorflow as tf

from constant import *


def _parse_serialized_example(serialized_example, num_features):
    """
    Parse serialized example proto.

    Input：
        serialized_example - serialized example proto
        num_features - number of features for each frame

    Output:
        parsed_context - a dictionary contains sequence label and sequence length
        parsed_feature - a dictionary contains sequence feature
    """

    context_features = {
        SEQUENCE_LENGTH: tf.FixedLenFeature([], dtype=tf.int64),
        LABEL: tf.VarLenFeature(dtype=tf.int64)
    }

    sequence_features = {
        FEATURE: tf.FixedLenSequenceFeature([num_features, ], dtype=tf.float32)
    }

    parsed_context, parsed_feature = tf.parse_single_sequence_example(
        serialized=serialized_example,
        context_features=context_features,
        sequence_features=sequence_features
    )

    return parsed_context, parsed_feature


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
    dataset = dataset.map(lambda x: _parse_serialized_example(x, num_features))
    dataset = dataset.shuffle(buffer_size=buffer_size)
    dataset = dataset.batch(batch_size=batch_size)
    dataset = dataset.repeat(count=num_epochs)
    iterator = dataset.make_one_shot_iterator()

    parsed_context, parsed_feature = iterator.get_next()

    features = {
        SEQUENCE_LENGTH: parsed_context[SEQUENCE_LENGTH],
        FEATURE: parsed_feature[FEATURE]
    }

    # CTC loss only takes int32
    labels = tf.cast(parsed_context[LABEL], dtype=tf.int32)

    return features, labels


def eval_input_fn():
    """
    Generate evaluation example

    Output:
        features - a dictionary contains sequence length and sequence feature
        labels - sequence label
    """

    dataset = tf.data.Dataset.from_tensor_slices({
        'feature': tf.constant(
            [
                [
                    [0],
                    [1]
                ],
                [
                    [1],
                    [0]
                ]
            ],
            dtype=tf.float32),
        'sequence_length': [2, 2]
    })

    dataset = dataset.batch(batch_size=1)

    iterator = dataset.make_one_shot_iterator()

    return iterator.get_next(), None
