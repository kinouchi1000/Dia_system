#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

#!/bin/bash
LINE_ACCESS_TOKEN="D5I9Qbe596RCLFnqZhfc8GfJ6kdHLp5oC3eYhUoCpFI"
function line_notify() {
  MESSAGE=$1
  curl -X POST -H "Authorization: Bearer ${LINE_ACCESS_TOKEN}" -F "message=$MESSAGE" https://notify-api.line.me/api/notify
}

line_notify "計算開始"

# NOTE: BTSJ
python ../transformers/examples/language-modeling/run_clm_edited.py \
    --model_name_or_path=rinna/japanese-gpt2-medium \
    --train_file=./kakikotoba_Data/BTSJ/data.train.txt \
    --validation_file=./kakikotoba_Data/BTSJ/data.validation.txt \
    --do_train \
    --do_eval \
    --num_train_epochs=50 \
    --save_total_limit=3 \
    --per_device_train_batch_size=1 \
    --per_device_eval_batch_size=1 \
    --output_dir='./output_prefine/output_kakiBTSJ' \
    --use_fast_tokenizer=False \
    --logging_dir='./logs/log_kakiBTSJ' \
    --logging_steps=500 \
    --save_steps=500 \
    --eval_steps=500 \
    || line_notify "エラーが発生しました"
line_notify "BTSJ終了"

# NOTE: CEJC
python ../transformers/examples/language-modeling/run_clm_edited.py \
    --model_name_or_path=rinna/japanese-gpt2-medium \
    --train_file=./kakikotoba_Data/CEJC/data.train.txt \
    --validation_file=./kakikotoba_Data/CEJC/data.validation.txt \
    --do_train \
    --do_eval \
    --num_train_epochs=50 \
    --save_total_limit=3 \
    --per_device_train_batch_size=1 \
    --per_device_eval_batch_size=1 \
    --output_dir='./output_prefine/output_kakiCEJC' \
    --use_fast_tokenizer=False \
    --logging_dir='./logs/log_kakiCEJC' \
    --logging_steps=500 \
    --save_steps=500 \
    --eval_steps=500 \
    || line_notify "エラーが発生しました"
    
line_notify "CEJC終了"

# NOTE: NUCC
python ../transformers/examples/language-modeling/run_clm_edited.py \
    --model_name_or_path=rinna/japanese-gpt2-medium \
    --train_file=./kakikotoba_Data/NUCC/data.train.txt \
    --validation_file=./kakikotoba_Data/NUCC/data.validation.txt \
    --do_train \
    --do_eval \
    --num_train_epochs=50 \
    --save_total_limit=3 \
    --per_device_train_batch_size=1 \
    --per_device_eval_batch_size=1 \
    --output_dir='./output_prefine/output_kakiNUCC' \
    --use_fast_tokenizer=False \
    --logging_dir='./logs/log_kakiNUCC' \
    --logging_steps=500 \
    --save_steps=500 \
    --eval_steps=500 \
    || line_notify "エラーが発生しました"

line_notify "NUCC終了"