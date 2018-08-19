# Author: caixuanting@gmail.com

import sys
from random import randint

import tensorflow as tf

from constant import FEATURE
from constant import LABEL
from constant import LENGTH


def write_example(filename, examples):
    """
    Write TFRecord into file.

    Input:
        filename - the file path
        examples - a list of example protos
    """

    writer = tf.python_io.TFRecordWriter(filename)

    for ex in examples:
        writer.write(ex.SerializeToString())

    writer.close()


def generate_sequence_example(feature, label):
    """
    Generate sequence examples according to feature and label

    Input:
        feature - the feature of the example
        label - the label of the example
    Output:
        example - protobufs of example
    """

    feature_list = [tf.train.Feature(float_list=tf.train.FloatList(value=f))
                    for f in feature]

    feature_dict = {FEATURE: tf.train.FeatureList(feature=feature_list)}

    sequence_features = tf.train.FeatureLists(feature_list=feature_dict)

    label_list = tf.train.Feature(
        int64_list=tf.train.Int64List(value=label))
    sequence_length_list = tf.train.Feature(
        int64_list=tf.train.Int64List(value=[len(feature)]))

    context_features = tf.train.Features(
        feature={LENGTH: sequence_length_list,
                 LABEL: label_list})

    example = tf.train.SequenceExample(context=context_features,
                                       feature_lists=sequence_features)

    return example


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python generate_example.py [file_path]')
        sys.exit(1)

    sequence_examples = []

    for _ in range(1000):
        feature = []
        label = []

        for _ in range(randint(1, 20)):
            feature.append([randint(0, 2)])

        label = [feature[0][0]]

        for f in feature:
            if f[0] != label[-1]:
                label.append(f[0])

        example = generate_sequence_example(feature, label)
        sequence_examples.append(example)

    write_example(sys.argv[1], sequence_examples)
