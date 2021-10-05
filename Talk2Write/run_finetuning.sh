#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

# NOTE: 
python ../transformers/examples/seq2seq/run_translation.py \
    --model_name_or_path megagonlabs/t5-base-japanese-web  \
    --do_train \
    --do_eval \
    --do_predict \
    --source_lang sp \
    --target_lang wr \
    --train_file ./data_reshaped_20210709/nucc_spoken2written_20210709.train.json \
    --validation_file ./data_reshaped_20210709/nucc_spoken2written_20210709.valid.json \
    --test_file ./data_reshaped_20210709/nucc_spoken2written_20210709.valid.json \
    --output_dir ./output_megagonalbs2 \
    --per_device_train_batch_size=4 \
    --per_device_eval_batch_size=4 \
    --overwrite_output_dir \
    --predict_with_generate \
    --max_train_samples 500 \
    --max_val_samples 500 \
    --logging_dir=log_magagonalbs2/ \
    --num_train_epochs 100
