# Author: caixuanting@gmail.com

import tensorflow as tf

from ctc_model_fn import lstm_model_fn
from constant import LSTM
from constant import MODEL_TYPE

MODEL_MAP = {
    LSTM: lstm_model_fn
}


def create_estimator(params):
    model_fn = MODEL_MAP[params[MODEL_TYPE]]

    return tf.estimator.Estimator(
        model_fn=model_fn,
        params=params
    )
