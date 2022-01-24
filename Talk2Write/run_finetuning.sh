#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

# LINE表示用
LINE_ACCESS_TOKEN="D5I9Qbe596RCLFnqZhfc8GfJ6kdHLp5oC3eYhUoCpFI"
function line_notify() {
  MESSAGE=$1
  curl -X POST -H "Authorization: Bearer ${LINE_ACCESS_TOKEN}" -F "message=$MESSAGE" https://notify-api.line.me/api/notify
}

function fine_tune(){
line_notify "$2:計算開始"
# NOTE: 
python ../transformers/examples/seq2seq/run_translation.py \
    --model_name_or_path "$1"  \
    --do_train \
    --do_eval \
    --do_predict \
    --source_lang sp \
    --target_lang wr \
    --train_file ./data/data_reshaped_20210709/nucc_spoken2written_20210709.train.json \
    --validation_file ./data/data_reshaped_20210709/nucc_spoken2written_20210709.valid.json \
    --test_file ./data/data_reshaped_20210709/nucc_spoken2written_20210709.valid.json \
    --output_dir "./model/$2" \
    --per_device_train_batch_size=4 \
    --per_device_eval_batch_size=4 \
    --max_val_samples 500 \
    --max_val_samples 500 \
    --save_total_limit 5
    --overwrite_output_dir \
    --predict_with_generate \
    --logging_dir="./logs/$2" \
    --logging_strategy steps \
    --logging_first_step true \
    --logging_steps 500 \
    --num_train_epochs 100 \
    --disable_tqdm false \
    --evaluation_strategy steps \
    || line_notify "計算失敗"
line_notify "$2:計算終了"
}

fine_tune "megagonlabs/t5-base-japanese-web" "megagonlabs_miss20211220"
# fine_tune "sonoisa/t5-base-japanese" "sonoisa_miss20211220"


