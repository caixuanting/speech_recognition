# Author: caixuanting@gmail.com

import unittest as ut

from parser import parse


class TestParseMethods(ut.TestCase):
    def test_parse(self):
        argv = [
            '--model_type', 'test_model',
            '--num_layers', '3',
            '--num_units', '7',
            '--num_classes', '11',
            '--filenames', 'a.txt', 'b.txt',
            '--num_features', '4',
            '--buffer_size', '5',
            '--batch_size', '100',
            '--num_epochs', '2',
            '--steps', '50'
        ]

        output = parse(argv)

        self.assertEqual('test_model', output.model_type)
        self.assertEqual(3, output.num_layers)
        self.assertEqual(7, output.num_units)
        self.assertEqual(11, output.num_classes)
        self.assertListEqual(['a.txt', 'b.txt'], output.filenames)
        self.assertEqual(4, output.num_features)
        self.assertEqual(5, output.buffer_size)
        self.assertEqual(100, output.batch_size)
        self.assertEqual(2, output.num_epochs)
        self.assertEqual(50, output.steps)


if __name__ == '__main__':
    ut.main()
