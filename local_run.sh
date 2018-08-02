#!/usr/bin/env bash

python local_pipeline.py \
       --model_type bilstm \
       --num_layers 1 \
       --num_units 20 \
       --num_classes 4 \
       --learning_rate 0.01 \
       --filenames test_data/sequence_examples.tfrecord \
       --num_features 1 \
       --buffer_size 100 \
       --batch_size 5 \
       --num_epochs 1000 \
       --steps 1 \
       --model_dir model/lstm_ctc