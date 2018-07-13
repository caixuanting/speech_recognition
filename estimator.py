import tensorflow as tf

from ctc_model_fn import lstm_model_fn

MODEL_MAP = {
    'lstm': lstm_model_fn
}


def create_estimator(params):
    model_fn = MODEL_MAP[params['model_type']]

    return tf.estimator.Estimator(
        model_fn = model_fn,
        params = params
    )
