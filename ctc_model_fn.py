import tensorflow as tf

def lstm_model_fn(features, labels, mode, params):
    audio_feature = features['audio_feature']
    sequence_length = features['sequence_length']

    cells = []

    for _ in range(params['num_layers']):
        cell = tf.contrib.rnn.LSTMCell(params['num_units'])
        cells.append(cell)

    stack = tf.contrib.rnn.MultiRNNCell(cells)

    outputs, state = tf.nn.dynamic_rnn(
        cell = stack,
        inputs = audio_feature,
        sequence_length = sequence_length,
        dtype = tf.float32
    )

    logits = tf.layers.dense(
        inputs = outputs,
        units = params['num_classes']
    )

    softmax = tf.nn.softmax(logits)
    
    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(
            mode = mode,
            predictions = {
                'softmax': softmax
            }
        )

    ctc_loss = tf.nn.ctc_loss(
        labels = labels,
        inputs = softmax,
        sequence_length = sequence_length,
        time_major = False
    )

    loss = tf.reduce_mean(ctc_loss)

    optimizer = tf.train.GradientDescentOptimizer(
        learning_rate = params['learning_rate']
    )

    train_op = optimizer.minimize(
        loss = loss,
        global_step = tf.train.get_global_step()
    )

    return tf.estimator.EstimatorSpec(
        mode = mode,
        loss = loss,
        train_op = train_op
    )
