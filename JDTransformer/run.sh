#! /bin/bash
# 仮想環境の起動
conda activate DSTS
# 対話システム実行
python scripts/dialog.py data/sample/bin/ \
 --path checkpoints/japanese-dialog-transformer-1.6B-empdial50k.pt \
 --beam 80 \
 --min-len 10 \
 --source-lang src \
 --target-lang dst \
 --tokenizer space \
 --bpe sentencepiece \
 --sentencepiece-model data/dicts/sp_oall_32k.model \
 --no-repeat-ngram-size 3 \
 --nbest 80 \
 --sampling \
 --sampling-topp 0.9 \
 --temperature 1.0 \
 --show-nbest 5
