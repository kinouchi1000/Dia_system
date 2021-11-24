#!/usr/bin/env python
# coding: utf-8

# import time
# import sys
# import re

import torch
from transformers import pipeline, AutoTokenizer, T5ForConditionalGeneration

# AutoModelForSeq2seqLM
# NOTEのまま！変更するべき

# モデルとトークナイザーの準備


class talk2write:

    # 各種ユーザー
    model = None        # 学習済みモデル
    tokenizer = None    # トークナイザー

    # コンストラクタ(初期化)

    def __init__(self, model_name, tokenizer_name):

        # ユーザの初期化
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    # 話し言葉から書き言葉へ変換
    def translate_t2w(self, text):
        # 入力データ整形
        text = text.replace("?", "？")

        # テキストをテンソルに変換
        inputs = self.tokenizer.encode(
            text, return_tensors="pt", max_length=512, truncation=True)
        output = ""
        # 推論
        self.model.eval()
        with torch.no_grad():
            output_ids = self.model.generate(inputs, max_length=200,
                                             no_repeat_ngram_size=5, num_beams=3)
            # \, max_length=100, min_length=5, length_penalty=5., num_beams=2)
            output = self.tokenizer.decode(output_ids[0])

            # データ整形
            output = output.replace("</s>", '')
            output = output.replace("<unk> ", '')
            output = output.replace("<pad> ", '')

        return output

# if __name__ == "__main__":
#     t2w = talk2write('./prefines/output_megagonalbs2', './prefines/output_megagonalbs2')

#     while 1:
#         #try:
#         sentence = input("input->>")
#         sentence = t2w.translate_t2w(sentence)
#         print("output->>"+sentence)
#         #except KeyboardInterrupt:
#         #    print("Ctrl+Cで停止しました")
#         #    break
#         #except:
#         #pass

# 対話モデルのコーパスを話し言葉に変換するときに使ったもの


if __name__ == "__main__":
    t2w = talk2write('./prefines/output_megagonalbs2',
                     './prefines/output_megagonalbs2')

    BTSJout = "../kakikotoba_Data/BTSJ/clean_all.csv"
    CEJCout = "../kakikotoba_Data/CEJC/clean_all.csv"
    NUCCout = "../kakikotoba_Data/NUCC/clean_all.csv"
    outD = [BTSJout, CEJCout, NUCCout]
    # BTSJ
    BTSJFile = "../ResponceGenerator/data/BTSJ_CSV/BTSJ_clean/data2/clean_all.csv"
    CEJCFile = "../ResponceGenerator/data/CEJC/CEJC_clean/data2/clean_all.csv"
    NUCCFile = "../ResponceGenerator/data/nucc/nucc_clean/data2/clean_all.csv"

    Directs = [BTSJFile, CEJCFile, NUCCFile]

    try:
        for D, outD in zip(Directs, outD):
            with open(D, 'r') as rf:
                with open(outD, 'w') as wf:
                    lines = rf.readlines()
                    for i, line in enumerate(lines):
                        if(line != '[EOD]'):
                            output = t2w.translate_t2w(line)
                            # ファイル書き込み
                            wf.write(output+'\n')
                            # debug
                            # if(i == 10):
                            #     break
                        else:
                            wf.write('[EOD]'+'\n')

    except OSError as e:
        print(e)
