# Author: caixuanting@gmail.com

import tensorflow as tf

from constant import BILSTM
from constant import LSTM
from constant import MODEL_DIR
from constant import MODEL_TYPE
from ctc_model_fn import bilstm_model_fn
from ctc_model_fn import lstm_model_fn

MODEL_MAP = {
    LSTM: lstm_model_fn,
    BILSTM: bilstm_model_fn
}


def create_estimator(params):
    """
    Create estimator for training

    Input:
        params - parameter dictionary for the model

    Output:
        estimator - estimator instance
    """

    model_fn = MODEL_MAP[params[MODEL_TYPE]]

    return tf.estimator.Estimator(
        model_fn=model_fn,
        model_dir=params[MODEL_DIR],
        params=params
    )
