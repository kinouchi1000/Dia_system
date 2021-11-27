#!/usr/bin/env python
# coding: utf-8

# import time
# import sys
# import re

from Wrapper.Treat_log import Logger
import torch
import datetime
import argparse
from logging import getLogger, StreamHandler, FileHandler, Formatter, DEBUG, WARN, INFO
from transformers import pipeline, AutoTokenizer, T5ForConditionalGeneration

# AutoModelForSeq2seqLM
# NOTEのまま！変更するべき

# モデルとトークナイザーの準備


def set_logger(name, dirname="log/main/"):
    dt_now = datetime.now()
    dt = dt_now.strftime('%Y%m%d_%H%M%S')
    fname = dirname + dt
    logger = getLogger(name)
    #handler1 = StreamHandler()
    #handler1.setFormatter(Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
    handler2 = FileHandler(filename=fname)
    handler2.setLevel(DEBUG)  # handler2はLevel.WARN以上
    handler2.setFormatter(
        Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
    # logger.addHandler(handler1)
    logger.addHandler(handler2)
    return logger


class talk2write:

    # 各種ユーザー
    model = None        # 学習済みモデル
    tokenizer = None    # トークナイザー

    # コンストラクタ(初期化)

    def __init__(self, args, Logger):

        # ユーザの初期化
        self.model = T5ForConditionalGeneration.from_pretrained(
            args.talk2write_model_dir)
        self.tokenizer = AutoTokenizer.from_pretrained(
            args.talk2write_tokenizer_dir)

        # ログ周り
        self.logger = Logger

    # 話し言葉から書き言葉へ変換
    def translate_t2w(self, text):
        self.logger.info("input:"+text)
        # 入力データ整形
        text = text.replace("?", "？")

        # テキストをテンソルに変換
        inputs = self.tokenizer.encode(
            text, return_tensors="pt", max_length=512, truncation=True)
        self.logger.info("encoded tensol:"+str(inputs))
        output = ""

        # 推論
        self.model.eval()
        with torch.no_grad():
            output_ids = self.model.generate(inputs, max_length=200,
                                             no_repeat_ngram_size=5, num_beams=3)
            # \, max_length=100, min_length=5, length_penalty=5., num_beams=2)
            output = self.tokenizer.decode(output_ids[0])
            self.logger.info("preFormat output:" + output)
            # データ整形
            output = output.replace("</s>", '')
            output = output.replace("<unk> ", '')
            output = output.replace("<pad> ", '')

        self.logger.info("output:"+output)

        return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--talk2write-model-dir', type=str,
                        help='Talk-to-Write model directory')
    parser.add_argument('--talk2write-tokenizer-dir', type=str,
                        help='Talk-to-Write tokenizer directory')
    args = parser.parse_args()

    Logger = set_logger("Talk2Write", "logs/generator/")

    t2w = talk2write(args, Logger)

    while 1:
        # try:
        sentence = input("input->>")
        sentence = t2w.translate_t2w(sentence)
        print("output->>"+sentence)
        # except KeyboardInterrupt:
        #    print("Ctrl+Cで停止しました")
        #    break
        # except:
        # pass

# 対話モデルのコーパスを話し言葉に変換するときに使ったもの


# if __name__ == "__main__":
#     t2w = talk2write('./prefines/output_megagonalbs2',
#                      './prefines/output_megagonalbs2')

#     BTSJout = "../kakikotoba_Data/BTSJ/clean_all.csv"
#     CEJCout = "../kakikotoba_Data/CEJC/clean_all.csv"
#     NUCCout = "../kakikotoba_Data/NUCC/clean_all.csv"
#     outD = [BTSJout, CEJCout, NUCCout]
#     # BTSJ
#     BTSJFile = "../ResponceGenerator/data/BTSJ_CSV/BTSJ_clean/data2/clean_all.csv"
#     CEJCFile = "../ResponceGenerator/data/CEJC/CEJC_clean/data2/clean_all.csv"
#     NUCCFile = "../ResponceGenerator/data/nucc/nucc_clean/data2/clean_all.csv"

#     Directs = [BTSJFile, CEJCFile, NUCCFile]

#     try:
#         for D, outD in zip(Directs, outD):
#             with open(D, 'r') as rf:
#                 with open(outD, 'w') as wf:
#                     lines = rf.readlines()
#                     for i, line in enumerate(lines):
#                         if(line != '[EOD]'):
#                             output = t2w.translate_t2w(line)
#                             # ファイル書き込み
#                             wf.write(output+'\n')
#                             # debug
#                             # if(i == 10):
#                             #     break
#                         else:
#                             wf.write('[EOD]'+'\n')

#     except OSError as e:
#         print(e)
