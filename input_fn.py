# Author: caixuanting@gmail.com

import tensorflow as tf

from constant import *

def _parse_serialized_example(serialized_example, num_features):
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

def input_fn(filenames, num_features, buffer_size, batch_size, num_epochs):
    dataset = tf.data.TFRecordDataset(filenames)
    dataset = dataset.map(lambda x : _parse_serialized_example(x, num_features))
    dataset = dataset.shuffle(buffer_size=buffer_size)
    dataset = dataset.batch(batch_size)
    dataset = dataset.repeat(num_epochs)
    iterator = dataset.make_one_shot_iterator()

    parsed_context, parsed_feature = iterator.get_next()

    features = {}

    features[SEQUENCE_LENGTH] = parsed_context[SEQUENCE_LENGTH]
    features[FEATURE] = parsed_feature[FEATURE]
    
    labels = parsed_context[LABEL]
    
    return features, labels


