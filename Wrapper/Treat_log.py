#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ログやコマンドライン表示用のクラス
"""
import datetime
import os
import shutil
import time
import pprint
import sys


DEBUG_SYSTEM_BOOL = True


class Logger:
    BASE = os.path.dirname(os.path.abspath(__file__))
    DEBUG_BOOL = DEBUG_SYSTEM_BOOL  # コマンドライン上にログを表示するかどうか
    dt_now = datetime.datetime.now()  # 使用時の時刻格納用
    my_time = 0  # 処理時間格納用
    be_my_time = 0  # 前回の処理時間格納用
    time_log = {}  # 任意の名前で処理時間格納用
    myname = ''  # 任意の名前

    # 初期化,名前の設定
    def __init__(self, name):
        # ログを出力するためのディレクトリを作成
        self.myname = os.path.normpath(os.path.join(
            self.BASE, '../Data/')) + "/Log/" + name
        dt_now = datetime.datetime.now()
        os.makedirs(self.myname, exist_ok=True)

        # ログ出力用のテキストファイルを作成
        self.myname = self.myname + "/" + \
            dt_now.strftime('%Y-%m-%d_%H:%M:%S') + ".txt"
        log_file = open(self.myname, "w", encoding="utf-8")
        log_file.close()

    """
    ログを出す
    """

    # ログを時間とともに表示,書き込む
    def add_log(self, sentence):
        dt_now = datetime.datetime.now()
        log_file = open(self.myname, "a", encoding="utf-8")
        log_file.write(dt_now.strftime('%Y-%m-%d_%H:%M:%S') +
                       ":" + str(sentence) + "\n")
        log_file.close()

    # ログをプロンプトに表示logにも追加
    def add_print_log(self, data):
        dt_now = datetime.datetime.now()
        sentence = ""
        if type(data) is list:
            for line in data:
                sentence += "/" + str(line)
        else:
            sentence = data
        if self.DEBUG_BOOL == True:
            print(dt_now.strftime('%Y-%m-%d_%H:%M:%S') + " : " + sentence)
        self.add_log(sentence)

    """
    プリントのみをする
    """

    # 引数を表示
    def print_sentence(self, sentence):
        if self.DEBUG_BOOL == True:
            print(sentence)

    # 引数のリストを縦に表示
    def print_list(self, list):
        if self.DEBUG_BOOL == True:
            for line in list:
                print(line)

    # 引数のリストを2つ並べて縦にプロンプトに表示
    def print_list_2row(self, list1, list2):
        if self.DEBUG_BOOL == True:
            for i in range(len(list1)):
                print(list1[i] + ":" + list2[i])

    # リストを綺麗に表示
    def print_pprint_list(self, list):
        if self.DEBUG_BOOL == True:
            pprint.pprint(list)

    """
    他機能
    """

    # 引数-1から0の間の経過時間を表示
    # sentence:動作箇所がわかるような文
    # 1:測定スタート,0:測定終了
    def count_time(self, sentence, cmd):
        if cmd == -1:
            self.time_log[sentence] = time.time()
        elif cmd == 0:
            self.my_time = time.time()
            string = sentence + " processed time:" + \
                str(self.my_time - self.time_log[sentence]) + " s"

            self.add_print_log(string)


# 動作確認用のクラス
class Hoge:
    logger = Logger('Hoge')

    def Func(self):
        self.logger.add_log('Add_log')
        self.logger.add_print_log('Add_print_log')
        self.logger.print_sentence('Print_sentence')
        self.logger.print_list(['A', 'B'])
        self.logger.print_list_2row(['A', 'B'], ['C', 'D'])
        self.logger.print_pprint_list([['A', 'B'], ['C', 'D']])
        self.logger.count_time('Hoge', -1)
        self.logger.count_time('Hoge', 0)

        # self.logger.Add_print_log(self.__class__.__name__ + "." + sys._getframe().f_code.co_name)


if __name__ == "__main__":
    hoge = Hoge()
    hoge.Func()
