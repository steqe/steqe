#!/bin/bash

export TRAIN_FILE=../data/for_t5/train/covid_temporal.txt
export TEST_FILE=../data/for_t5/test/covid_temporal.txt

venv_t5/bin/python train_t5.py \
    --output_dir=spatial_covid_seed10 \
    --model_type=t5 \
    --tokenizer_name=t5-large \
    --model_name_or_path=t5-large \
    --do_train \
    --do_eval \
    --num_train_epochs=20 \
    --train_data_file=$TRAIN_FILE \
    --eval_data_file=$TEST_FILE \
    --line_by_line \
    --per_gpu_train_batch_size=2 \
    --per_device_train_batch_size=2 \
    --gradient_accumulation_steps=16 \
    --per_device_eval_batch_size=4 \
    --per_gpu_eval_batch_size=4 \
    --save_steps=50000 \
    --seed=10 \
    --logging_steps=1000 \
    --overwrite_output_dir