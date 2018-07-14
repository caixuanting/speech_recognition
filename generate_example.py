# Author: caixuanting@gmail.com
import sys

import tensorflow as tf

from google.protobuf import text_format

from constant import *

def write_example(filename, examples):
    '''
    Write TFRecord into file.

    Input:
        filename - the file path
        examples - a list of examples
    '''
    writer = tf.python_io.TFRecordWriter(filename)

    for example in examples:
        writer.write(example.SerializeToString())

    writer.close()


def generate_sequence_example(feature, label):
    '''
    Generate sequence examples according to feature and label

    Input:
        feature - the feature of the example
        label - the label of the example
    '''
    feature_list = [tf.train.Feature(float_list=tf.train.FloatList(value=f))
                    for f in feature]

    feature_dict = {FEATURE: tf.train.FeatureList(feature=feature_list)}

    sequence_features = tf.train.FeatureLists(feature_list=feature_dict)

    label_list = tf.train.Feature(
        int64_list=tf.train.Int64List(value=label))
    sequence_length_list = tf.train.Feature(
        int64_list=tf.train.Int64List(value=[len(feature)]))
    
    context_features = tf.train.Features(
        feature={SEQUENCE_LENGTH: sequence_length_list,
                 LABEL: label_list})

    example = tf.train.SequenceExample(context=context_features,
                                       feature_lists=sequence_features)

    return example


if __name__ == '__main__':
    sequence_examples = []
    
    sequence_examples.append(
        generate_sequence_example(
            [[0, 0], [0, 0], [1, 1], [1, 1]],
            [0, 1]
        )
    )

    sequence_examples.append(
        generate_sequence_example(
            [[0, 0], [1, 1], [1, 1], [1, 1]],
            [0, 1]
        )
    )

    sequence_examples.append(
        generate_sequence_example(
            [[1, 1], [1, 1], [0, 0], [0, 0]],
            [1, 0]
        )
    )

    sequence_examples.append(
        generate_sequence_example(
            [[1, 1], [1, 1], [1, 1], [0, 0]],
            [1, 0]
        )
    )
        
    write_example(sys.argv[1], sequence_examples)
