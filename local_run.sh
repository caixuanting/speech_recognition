#!/usr/bin/env bash

python local_pipeline.py \
       --model_type lstm \
       --num_layers 2 \
       --num_units 20 \
       --num_classes 4 \
       --learning_rate 0.01 \
       --filenames test_data/sequence_examples.tfrecord \
       --num_features 1 \
       --buffer_size 1 \
       --batch_size 1 \
       --num_epochs 100 \
       --steps 10000