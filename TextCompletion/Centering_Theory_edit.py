#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
過去の発話を利用して話題を補完するクラス
'''
import sys
import re
import threading
import readline
from datetime import datetime
from logging import getLogger, StreamHandler, FileHandler, Formatter, DEBUG, WARN, INFO
from colorama import Fore, Back, Style

from dic import particle_dic, AVOID_WORD_LIST, FOLLOW_WORD_LIST, Not_noun_words, else_anaphor_words

try:
    from .caseFrame.xml_SQ import XML_SQ
    from .Wrapper.Treat_mecab import Mecab
    from .Wrapper.Treat_CaboCha import Cabocha
except:
    from caseFrame.xml_SQ import XML_SQ
    from Wrapper.Treat_mecab import Mecab
    from Wrapper.Treat_CaboCha import Cabocha


class Centering_Theory:
    # 各種ユーザー
    logger = None  # ログ保存用
    mecab_user = None  # MeCab使用用
    Cabocha_user = None  # CaboCha使用用
    SQ_usr = None  # 格フレーム検索用

    Cp_list = None  # Cp
    TRANSITION_list = []  # 状態変異のリスト
    Cb = None  # Cbの履歴
    Ob_list = []  # 目的語の先行詞のリスト
    ZeroPart = 0  # 先行詞の探索を行うかどうかの判定(0なら行う)
    My_your = 0  # 発話者を把握するフラグ
    Center_count = 0  # 中心化理論の実行回数

    def __init__(self, Logger, DBPath='TextCompletion/caseFrame/example.db'):
        # ユーザーの初期化
        self.logger = Logger
        self.mecab_user = Mecab()
        self.Cabocha_user = Cabocha()
        self.SQ_usr = XML_SQ(DBPath)

    def main(self, sentence, usr_id):
        # 2文以上で構成されていたら、「。」で分割 -- 20211129
        print(sentence)
        sentenceList = re.split('(?<=[。！？!?.])', sentence)
        if '' in sentenceList:
            sentenceList.remove('')
        self.logger.info('input:'+str(sentenceList))

        # start
        output = ''
        for s in sentenceList:
            self.logger.info('text:' + s + ' user->' + str(usr_id))
        #     s = self.Follow_Zero_Part(s, usr_id)  # ゼロ代名詞の補い
        #     if self.ZeroPart == 0:
        #         self.Centering(s, usr_id)  # 中心化理論
        #         self.Objectum(s)  # 目的語の先行詞の探索
        #     self.ZeroPart = 0
        #     output += s
        # self.logger.info('result:'+output)
        return output

     # ゼロ代名詞の補い

    def Follow_word(
            self,
            sentence,
            follow_word,
            fell_part,
            particle,
            Do_word,
            usr_id):
        # 形態素解析を行う
        wakati, part = self.mecab_user.get_word_part_list(sentence)
        part = [y.split('-')[0] for y in part]
        # print(part)

        # 「あなた」と「私」の変換
        # print('My_your:'+str(self.My_your)+'->usr_id:'+str(usr_id))
        if self.My_your != usr_id:
            if 'あなた' in follow_word:
                follow_word = '私'
            elif '私' in follow_word:
                follow_word = 'あなた'
            self.My_your = usr_id

        # 格フレームに基づいたゼロ代名詞の補い
        if particle != 'は':
            # print('<Frame-Follow>')
            sentence = ''
            frame_sentence = ''

            # 述語を分かち書きしたリストを作成
            Do = self.mecab_user.get_wakatied_sentence(Do_word)
            Do = Do.split()

            # 目的語と格助詞を組み合わせる
            for word in wakati:
                if word in Do[0]:
                    frame_sentence = follow_word + particle + word
                    sentence += frame_sentence
                else:
                    sentence += word

        # 感動詞、接続詞があるなら、そのあとに文章を補う
        else:
            if fell_part:
                # print('<Fell-Follow>')
                sentence = ''
                fell_sentence = ''
                for word, w_p in zip(wakati, part):
                    if w_p == '接続詞' or w_p == '感動詞':
                        # print(w_p)
                        fell_sentence = word + follow_word + 'は'
                        sentence += fell_sentence
                    else:
                        sentence += word

            # 通常のゼロ代名詞補い
            else:
                # print('<nomal-Follow>')
                sentence = follow_word + 'は' + sentence

        return sentence

    # 代名詞の先行詞を見つける
    def Category_check(self, word, Cb_list):
        next_word = ''
        for Cb in Cb_list:
            # print(Cb)
            Category = self.mecab_user.get_part_id(Cb)
            anaphor_word = self.else_anaphor_words[word]
            # 三人称
            if anaphor_word == 0:
                if '人名' in Category:
                    next_word = Cb
            # 「そちら、こちら」など
            elif anaphor_word == 1:
                if '地域' in Category:
                    next_word = Cb
            # 「これ、それ、あれ」など
            elif anaphor_word == 2:
                if '人名' not in Category and '地域' not in Category:
                    if Cb not in self.else_anaphor_words:
                        if '一般' in Category:
                            next_word = Cb
                        elif 'サ変接続' in Category:
                            next_word = Cb
        return next_word

    # SQlite3の接続をcloseする#############################

    def close(self):
        self.SQ_usr.close()

    # 中心化理論の要素をリセットする#############################
    def Forget_centering_element(self):
        # print('<Forget_centering_element!!>')
        self.Cp_list = []  # Cpのリスト
        self.TRANSITION_list = []  # 状態変異のリスト
        self.Cb_list = []  # Cbのリスト
        self.Ob_list = []  # 目的語の先行詞のリスト


def set_logger(name, dirname='log/main/'):
    dt_now = datetime.now()
    dt = dt_now.strftime('%Y%m%d_%H%M%S')
    fname = dirname + dt
    logger = getLogger(name)
    #handler1 = StreamHandler()
    #handler1.setFormatter(Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s'))
    handler2 = FileHandler(filename=fname)
    handler2.setLevel(DEBUG)  # handler2はLevel.WARN以上
    handler2.setFormatter(
        Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s'))
    # logger.addHandler(handler1)
    logger.addHandler(handler2)
    logger.setLevel(DEBUG)
    return logger


def main():
    logger = set_logger('CenteringTheory', 'log/')
    Center = Centering_Theory(logger, 'caseFrame/example.db')
    usr = 0
    while 1:
        try:
            sentence = input('input->>')

            sentence = Center.Centering_Word(sentence, usr)
            print('output->>'+sentence)
        except KeyboardInterrupt:
            print('\nCtrl+Cで停止しました')
            Center.close()
            break
        except Exception as e:
            print(e)
            sys.exit(0)


if __name__ == '__main__':
    main()
