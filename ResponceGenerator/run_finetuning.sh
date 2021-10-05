#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

# NOTE: 
python ../transformers/examples/language-modeling/run_clm_edited.py \
    --model_name_or_path=./nttcslab/japanese-dialog-transformers \
    --train_file=./data/mixed_BTSJ_CEJC_nucc/data2/mixed.train.txt \
    --validation_file=./data/mixed_BTSJ_CEJC_nucc/data2/mixed.valid.txt \
    --do_train \
    --do_eval \
    --num_train_epochs=50 \
    --save_total_limit=3 \
    --per_device_train_batch_size=1 \
    --per_device_eval_batch_size=1 \
    --output_dir='./output_prefine/output_sameDialogerConnect_NTT' \
    --use_fast_tokenizer=False \
    --logging_dir='./logs/log_sameDialogerConnect_NTT' \
    --logging_steps=500 \
    --save_steps=500 \
    --eval_steps=500
