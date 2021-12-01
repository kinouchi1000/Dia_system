#! /bin/bash

cd ~/Dia_system
# 仮想環境の起動
. /home/kinouchitakahiro/anaconda3/etc/profile.d/conda.sh && conda deactivate && conda activate DSTS

# 対話システム実行
# DIALOGUE_MODEL=checkpoints/japanese-dialog-transformer-1.6B-empdial50k.pt
DIALOGUE_MODEL=checkpoints/japanese-dialog-transformer-1.6B-persona50k.pt

python scripts/dialog.py data/sample/bin/ \
 --path $DIALOGUE_MODEL\
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
