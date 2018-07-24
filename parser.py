# Author: caixuanting@gmail.com

import argparse

from constant import LEARNING_RATE
from constant import MODEL_TYPE
from constant import NUM_LAYERS
from constant import NUM_UNITS
from constant import NUM_CLASSES


def parse(argv):
    """
    Parse parameters from list of arguments

    Input:
        argv - list of arguments
    Output:
        namespace - a namespace with parsed parameters
    """

    parser = argparse.ArgumentParser(description='Parameters for the system')

    parser.add_argument('--model_type')
    parser.add_argument('--num_layers', type=int)
    parser.add_argument('--num_units', type=int)
    parser.add_argument('--num_classes', type=int)
    parser.add_argument('--learning_rate', type=float)
    parser.add_argument('--filenames', metavar='F', nargs='+')
    parser.add_argument('--num_features', type=int)
    parser.add_argument('--buffer_size', type=int)
    parser.add_argument('--batch_size', type=int)
    parser.add_argument('--num_epochs', type=int)
    parser.add_argument('--steps', type=int)

    # parser.add_argument('--', type=int)

    return parser.parse_args(argv)


def create_params(namespace):
    params = {
        LEARNING_RATE: namespace.learning_rate,
        MODEL_TYPE: namespace.model_type,
        NUM_LAYERS: namespace.num_layers,
        NUM_UNITS: namespace.num_units,
        NUM_CLASSES: namespace.num_classes,
    }

    return params
