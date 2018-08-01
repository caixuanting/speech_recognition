# Author: caixuanting@gmail.com

import unittest as ut

from estimator import create_estimator


class TestCreateEstimatorMethods(ut.TestCase):
    def test_create_estimator(self):
        params = {
            'model_type': 'lstm',
            'num_layers': 1,
            'num_units': 10,
            'num_classes': 3,
            'learning_rate': 0.01,
            'model_dir': 'test'
        }

        estimator = create_estimator(params)

        self.assertEqual('test', estimator.model_dir)


if __name__ == '__main__':
    ut.main()
