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

    cells = [tf.contrib.rnn.LSTMCell(params[NUM_UNITS]) for _ in range(params[NUM_LAYERS])]

    stack = tf.contrib.rnn.MultiRNNCell(cells)

    outputs, state = tf.nn.dynamic_rnn(
        inputs=feature,
        cell=stack,
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


def bilstm_model_fn(features, labels, mode, params):
    feature = features[FEATURE]

    # CTC loss only takes int32
    sequence_length = tf.cast(features[LENGTH], dtype=tf.int32)

    fw_cells = [tf.contrib.rnn.LSTMCell(params[NUM_UNITS]) for _ in range(params[NUM_LAYERS])]
    bw_cells = [tf.contrib.rnn.LSTMCell(params[NUM_UNITS]) for _ in range(params[NUM_LAYERS])]

    fw_stack = tf.contrib.rnn.MultiRNNCell(fw_cells)
    bw_stack = tf.contrib.rnn.MultiRNNCell(bw_cells)

    (fw_output, bw_output), state = tf.nn.bidirectional_dynamic_rnn(
        cell_fw=fw_stack,
        cell_bw=bw_stack,
        inputs=feature,
        sequence_length=sequence_length,
        dtype=tf.float32
    )

    outputs = tf.concat(values=[fw_output, bw_output], axis=-1)

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