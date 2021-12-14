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

FILE_NAME=kakikotobaNUCC
line_notify "計算開始"
# NOTE: NUCC
python ../transformers/examples/language-modeling/run_clm_edited.py \
    --model_name_or_path=rinna/japanese-gpt2-medium \
    --train_file=./kakikotoba_Data/NUCC/data.train.txt \
    --validation_file=./kakikotoba_Data/NUCC/data.validation.txt \
    --do_train \
    --do_eval \
    --num_train_epochs=9 \
    --save_total_limit=5 \
    --per_device_train_batch_size=1 \
    --per_device_eval_batch_size=1 \
    --output_dir="./model/${FILE_NAME}" \
    --use_fast_tokenizer=False \
    --logging_dir="./logs/${FILE_NAME}" \
    --logging_steps=500 \
    --logging_strategy steps \
    --logging_first_step true \
    --save_steps=1000 \
    --eval_steps=500 \
    --evaluation_strategy steps \
    || line_notify "エラーが発生しました"

line_notify "NUCC終了"

# Note:
# 初期段階では５０エポックにしていたが、過学習が起きているため、8−9くらいにした。
