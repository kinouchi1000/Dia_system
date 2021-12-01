#! /bin/bash

set -eu

# DIALOGUE_MODEL=JDTransformer/checkpoints/japanese-dialog-transformer-1.6B-empdial50k.pt
DIALOGUE_MODEL=JDTransformer/checkpoints/japanese-dialog-transformer-1.6B-persona50k.pt

# 仮想環境の起動＊＊＊人によって違うので、注意！
. /home/kinouchitakahiro/anaconda3/etc/profile.d/conda.sh && conda deactivate && conda activate DSTS

# 対話システム実行
python Dia_system.py JDTransformer/data/sample/bin/ \
  --path $DIALOGUE_MODEL \
  --beam 80 \
  --min-len 10 \
  --source-lang src \
  --target-lang dst \
  --tokenizer space \
  --bpe sentencepiece \
  --sentencepiece-model JDTransformer/data/dicts/sp_oall_32k.model \
  --no-repeat-ngram-size 3 \
  --nbest 80 \
  --sampling \
  --sampling-topp 0.9 \
  --temperature 1.0 \
  --show-nbest 5 \
  --use-talk2write-model True \
  --talk2write-model-dir ./Talk2Write/model/output_megagonalbs2 \
  --talk2write-tokenizer-dir ./Talk2Write/model/output_megagonalbs2 \
  --use-centering-method True \

