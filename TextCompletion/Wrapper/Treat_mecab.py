#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
mecabの品詞IDのリスト
その他,間投,*,* 0
フィラー,*,*,* 1
感動詞,*,*,* 2
記号,アルファベット,*,* 3
記号,一般,*,* 4
記号,括弧開,*,* 5
記号,括弧閉,*,* 6
記号,句点,*,* 7
記号,空白,*,* 8
記号,読点,*,* 9
形容詞,自立,*,* 10
形容詞,接尾,*,* 11
形容詞,非自立,*,* 12
助詞,格助詞,一般,* 13
助詞,格助詞,引用,* 14
助詞,格助詞,連語,* 15
助詞,係助詞,*,* 16
助詞,終助詞,*,* 17
助詞,接続助詞,*,* 18
助詞,特殊,*,* 19
助詞,副詞化,*,* 20
助詞,副助詞,*,* 21
助詞,副助詞／並立助詞／終助詞,*,* 22
助詞,並立助詞,*,* 23
助詞,連体化,*,* 24
助動詞,*,*,* 25
接続詞,*,*,* 26
接頭詞,形容詞接続,*,* 27
接頭詞,数接続,*,* 28
接頭詞,動詞接続,*,* 29
接頭詞,名詞接続,*,* 30
動詞,自立,*,* 31
動詞,接尾,*,* 32
動詞,非自立,*,* 33
副詞,一般,*,* 34
副詞,助詞類接続,*,* 35
名詞,サ変接続,*,* 36
名詞,ナイ形容詞語幹,*,* 37
名詞,一般,*,* 38
名詞,引用文字列,*,* 39
名詞,形容動詞語幹,*,* 40
名詞,固有名詞,一般,* 41
名詞,固有名詞,人名,一般 42
名詞,固有名詞,人名,姓 43
名詞,固有名詞,人名,名 44
名詞,固有名詞,組織,* 45
名詞,固有名詞,地域,一般 46
名詞,固有名詞,地域,国 47
名詞,数,*,* 48
名詞,接続詞的,*,* 49
名詞,接尾,サ変接続,* 50
名詞,接尾,一般,* 51
名詞,接尾,形容動詞語幹,* 52
名詞,接尾,助数詞,* 53
名詞,接尾,助動詞語幹,* 54
名詞,接尾,人名,* 55
名詞,接尾,地域,* 56
名詞,接尾,特殊,* 57
名詞,接尾,副詞可能,* 58
名詞,代名詞,一般,* 59
名詞,代名詞,縮約,* 60
名詞,動詞非自立的,*,* 61
名詞,特殊,助動詞語幹,* 62
名詞,非自立,一般,* 63
名詞,非自立,形容動詞語幹,* 64
名詞,非自立,助動詞語幹,* 65
名詞,非自立,副詞可能,* 66
名詞,副詞可能,*,* 67
連体詞,*,*,* 68
"""
import MeCab
import re
from tqdm import tqdm


# MeCabを使うためのクラス
class Mecab:
    # 各種ユーザー
    mecab_tagger_chasen = None
    mecab_tagger_wakati = None
    file_user = None

    # 形態素解析用の辞書の場所
    MECAB_NEOLOGD_DIC_PATH = '/home/kinouchitakahiro/anaconda3/envs/DSTS/lib/mecab/dic/mecab-ipadic-neologd'

    # 変格活用の辞書の定義
    conjugation_dic = {
        '基本形': 1,
        '未然形': 2,
        '連用形': 3,
        '仮定形': 4,
        '命令ｅ': 5,
        '連用タ接続': 6
    }

    # 解析器を用意
    def __init__(self):
        self.mecab_tagger_chasen = MeCab.Tagger(
            "-Ochasen -d " + self.MECAB_NEOLOGD_DIC_PATH)
        self.mecab_tagger_wakati = MeCab.Tagger(
            "-Owakati -d " + self.MECAB_NEOLOGD_DIC_PATH)
        self.mecab_tagger_ID = MeCab.Tagger(
            "-F\"%h\" -E\"\n\"" + self.MECAB_NEOLOGD_DIC_PATH)

    # 分かち書きした文を返す
    def get_wakatied_sentence(self, sentence):
        sentence = str(sentence)
        sentence = self.mecab_tagger_wakati.parse(sentence)
        sentence = re.sub('\n', '', sentence)
        return sentence

    # 引数の単語の品詞を返す
    def get_part(self, word):
        node = self.mecab_tagger_chasen.parseToNode(word)
        node = node.next
        node_info = node.feature.split(",")
        if len(node_info) >= 8:
            word = node_info[0]

        return word

    # 引数の単語の品詞IDを返す
    def get_part_id(self, word):
        node = self.mecab_tagger_chasen.parseToNode(word)
        node = node.next
        node_info = node.feature

        return node_info

    # 引数の単語の原型を返す
    def get_original_word(self, word):
        node = self.mecab_tagger_chasen.parseToNode(word)
        node = node.next
        node_info = node.feature.split(",")
        word = None
        if len(node_info) >= 8:
            word = node.feature.split(",")[6]

        return word

    # 文を引数に取る
    # 分かち書きした後の単語のリストとその品詞のリストを返す
    def get_word_part_list(self, sentence):
        word_list = []
        part_list = []

        info = self.mecab_tagger_chasen.parse(sentence)
        info_list = info.split('\n')
        info_list = [x.split('\t') for x in info_list]
        for sub in info_list:
            if sub[0] != 'EOS' and sub[0] != '':
                word_list.append(sub[0])
                part_list.append(sub[3])
        return word_list, part_list

    # 用言の標準形を返す
    def get_word_nomal(self, sentence):
        info = self.mecab_tagger_chasen.parse(sentence)
        info_list = info.split('\n')
        info_list = [x.split('\t') for x in info_list]
        print(info_list)
        for sub in info_list:
            if sub[0] != 'EOS' and sub[0] != '':
                word = sub[2]
        return word


if __name__ == "__main__":
    user = Mecab()
    while True:
        i = input('input:')
        original = user.get_part_id(i)
        print(original)
