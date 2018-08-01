# Author: caixuanting@gmail.com

import tensorflow as tf

from constant import FEATURE
from constant import LEARNING_RATE
from constant import LENGTH
from constant import NUM_CLASSES
from constant import NUM_LAYERS
from constant import NUM_UNITS
from constant import SOFTMAX


def lstm_model_fn(features, labels, mode, params):
    feature = features[FEATURE]

    # CTC loss only takes int32
    sequence_length = tf.cast(features[LENGTH], dtype=tf.int32)

    cells = []

    for _ in range(params[NUM_LAYERS]):
        cell = tf.contrib.rnn.LSTMCell(params[NUM_UNITS])
        cells.append(cell)

    stack = tf.contrib.rnn.MultiRNNCell(cells)

    outputs, state = tf.nn.dynamic_rnn(
        cell=stack,
        inputs=feature,
        sequence_length=sequence_length,
        dtype=tf.float32
    )

    logits = tf.layers.dense(
        inputs=outputs,
        units=params[NUM_CLASSES]
    )

    softmax = tf.nn.softmax(logits)

    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(
            mode=mode,
            predictions={
                SOFTMAX: softmax
            }
        )

    ctc_loss = tf.nn.ctc_loss(
        labels=labels,
        inputs=softmax,
        sequence_length=sequence_length,
        time_major=False
    )

    loss = tf.reduce_mean(ctc_loss)

    optimizer = tf.train.GradientDescentOptimizer(
        learning_rate=params[LEARNING_RATE]
    )

    train_op = optimizer.minimize(
        loss=loss,
        global_step=tf.train.get_global_step()
    )

    return tf.estimator.EstimatorSpec(
        mode=mode,
        loss=loss,
        train_op=train_op
    )
