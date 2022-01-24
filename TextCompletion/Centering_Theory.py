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

    talk2write_Bool = True  # 話し言葉→書き言葉切り替え用

    Cp_list = []  # Cpのリスト
    TRANSITION_list = []  # 状態変異のリスト
    Cb_list = []  # Cbのリスト
    Ob_list = []  # 目的語の先行詞のリスト

    # 特定の助詞と先行詞の格納場所
    particle_dic = {
        'は': 0,
        'が': 1,
        'も': 2,
        'に': 3,
        'を': 4,
        'の': 4,
        'へ': 4,
        'と': 4,
        'から': 4,
        'より': 4,
        'で': 4,
        'って': 4,
        'やら': 4,
        'か': 4,
        'なり': 4,
        'だの': 4,
        'ばかり': 4,
        'まで': 4,
        'だけ': 4,
        'ほど': 4,
        'くらい': 4,
        'ぐらい': 4,
        'など': 4,
        'こそ': 4,
        'でも': 4,
        'しか': 4,
        'さえ': 4,
        'だに': 4,
    }

    # 単語として分類されても,先行詞には用いない単語
    AVOID_WORD_LIST = [
        'あ',
        'う',
        'お',
        'せ',
        'する',
        'ください',
        'られ',
        'だ',
        'いる',
        'です',
        'ます',
        '何'
    ]

    # 単語として分類された場合、先行詞を補う単語
    FOLLOW_WORD_LIST = [
        'もの',
        'こと',
        'の',
    ]

    Not_noun_words = [
        'どれ',
        'どこ',
        'なに',  # 2021.12 kinouchi
    ]

    # 照応詞の辞書(三人称のみ)
    else_anaphor_words = {
        '彼': 0,
        '彼ら': 0,
        '彼女': 0,
        '彼女ら': 0,
        '彼女たち': 0,
        'こいつ': 0,
        '此奴': 0,
        'そいつ': 0,
        '其奴': 0,
        'あいつ': 0,
        '彼奴': 0,
        'そこ': 1,
        'そちら': 1,
        'そっち': 1,
        'こちら': 1,
        'こっち': 1,
        'これ': 2,
        'これら': 2,
        'それ': 2,
        'その': 2,  # 2021.12 kinouchi
        'それら': 2,
        'あれ': 2,
        'あの': 2,  # 2021.12 kinouchi
        'あれら': 2,
    }

    O_index = 0  # Obのインデックス
    index = 0  # Cbのインデックス
    ZeroPart = 0  # 先行詞の探索を行うかどうかの判定(0なら行う)
    My_your = 0  # 発話者を把握するフラグ
    Center_count = 0  # 中心化理論の実行回数

    # 初期化#############################################################
    def __init__(self, Logger, DBPath='TextCompletion/caseFrame/example.db'):
        # ユーザーの初期化
        self.logger = Logger
        self.mecab_user = Mecab()
        self.Cabocha_user = Cabocha()
        self.SQ_usr = XML_SQ(DBPath)

    # 中心化理論を用いて、文章を補う####################################
    def Centering_Word(self, sentence, usr_id):

        # 2文以上で構成されていたら、「。」で分割 -- 20211129
        print(sentence)
        sentenceList = re.split('(?<=[。！？!?.])', sentence)
        if '' in sentenceList:
            sentenceList.remove('')
        self.logger.info('input:'+str(sentenceList))

        output = ''
        # 照応解析開始
        for s in sentenceList:
            self.logger.info('text:' + s + ' user->' + str(usr_id))
            s = self.Follow_Zero_Part(s, usr_id)  # ゼロ代名詞の補い
            if self.ZeroPart == 0:
                self.Centering(s, usr_id)  # 中心化理論
                self.Objectum(s)  # 目的語の先行詞の探索
            self.ZeroPart = 0
            output += s
        self.logger.info('result:'+output)
        return output

    # ゼロ代名詞を求め、文章を補う##############################################
    def Follow_Zero_Part(self, sentence, usr_id):

        self.logger.info('----------Zero_Part_start----------')
        # 形態素解析を行う
        wakati, part = self.mecab_user.get_word_part_list(sentence)
        part = [y.split('-') for y in part]
        self.logger.info('Word_list->' + str(wakati))

        # 条件を満たしているかの判定
        Follow_Name = False  # 代名詞
        Main_part = False  # 助詞(主題、ガ格)
        particle_part = False  # その他の助詞
        Do_part = False  # 動詞,形容詞
        fell_part = False  # 感動詞,接続詞
        Nane_follow_part = False  # 名詞 + 助動詞
        Ob_Follow = False  # ゼロ代名詞の補い
        Do_word = ''

        # 文を補う条件を満たしているか、品詞によって判定
        for num, word in enumerate(wakati):
            w_class = part[num][0]
            pre_class = part[num - 1][0]
            # 名詞
            if w_class == '名詞' and word in self.else_anaphor_words:
                # 三人称の代名詞
                Follow_Name = True
            # 動詞、形容詞
            elif w_class == '動詞' or w_class == '形容詞':
                Do_part = True
            # 助詞
            elif w_class == '助詞':
                # 終助詞と接続助詞は対象に除く
                if '終助詞' not in part[num][1] and '接続助詞' not in part[num][1]:
                    # 主題が存在し、助動詞、助詞が前の単語に無い場合
                    if word == 'は' or word == 'が' or word == 'も':
                        if pre_class != '助動詞' and pre_class != '助詞':
                            Main_part = True
                        else:
                            particle_part = True
                    else:
                        particle_part = True
            # 接続詞,感動詞
            elif w_class == '接続詞' or w_class == '感動詞':
                fell_part = True
            # 助動詞
            elif w_class == '助動詞':
                if pre_class == '名詞':
                    if part[num - 1][1] != '非自立':
                        Nane_follow_part = True

        # はじめの発話は,ゼロ代名詞を補わない
        if len(self.Cb_list) == 0:
            Cb = ''
        else:
            Cb = self.Cb_list[-1]

        # 主題のゼロ代名詞を補う
        if not Main_part:
            self.logger.info('Not in 「は」、「が」')
            # 動詞、形容詞があれば補う
            if Do_part or Nane_follow_part:
                self.logger.info('Word in 動詞,形容詞,名詞+助動詞')
                if Cb != '':
                    sentence = self.Follow_word(
                        sentence, Cb, fell_part, 'は', None, usr_id
                    )
                    self.ZeroPart = 0
                else:
                    if particle_part:
                        self.ZeroPart = 0
                    else:
                        self.ZeroPart = 1
            elif particle_part == False:
                self.ZeroPart = 1

        # 簡単な照応解析
        if Cb != '':
            if Follow_Name:
                sentence = self.anaphoric_analysis_Center(sentence)

        # 主題が同定、もしくは助動詞が存在する場合
        if self.ZeroPart == 0 and usr_id == 0:
            if Do_part or Nane_follow_part:

                # CaboChaによりかかり受けの関係を調べる
                word_list = self.Cabocha_user.get_chunks(sentence)
                len_word = len(word_list)
                for i in range(len_word):
                    Fo1_word = word_list[i][0]
                    Fo2_word = word_list[i][1]
                    # 係り元の形態素解析を行う
                    self.logger.info(
                        'Pair:(' + str(Fo1_word) + ' → ' + str(Fo2_word) + ')'
                    )
                    w_word, w_part = self.mecab_user.get_word_part_list(
                        Fo1_word)
                    w_part = [y.split('-')[0] for y in w_part]

                    # かかり先の標準形を返す
                    word = self.mecab_user.get_original_word(Fo2_word)
                    # もし、かかり先の標準形がない(None)なら、Fo2_wordをそのまま入れる

                    if word is None:
                        word = Fo2_word

                    # 品詞のリストを取得
                    word_part = self.mecab_user.get_part_id(word)
                    word_part = word_part.split(',')

                    # 現在の単語の品詞
                    N_word_part = word_part[0]

                    # 動詞,形容詞
                    if N_word_part == '動詞' or N_word_part == '形容詞':
                        if w_part[0] == '名詞':
                            Do_word = word
                            Do_word_all = Fo2_word

                    # 名詞
                    elif N_word_part == '名詞':
                        if word_part[1] == 'サ変接続' or word_part[1] == '形容動詞語幹':
                            if w_part[0] == '名詞':
                                Do_word = word
                                Do_word_all = Fo2_word

                # 対象の述語がある場合
                if Do_word != '' and Do_word not in self.Not_noun_words:
                    for i, (word, part) in enumerate(zip(w_word, w_part)):
                        if part == '助詞':
                            if 'は' not in word and 'も' not in word:
                                if w_part[i - 1] == '名詞':
                                    Ob_Follow = True

            # 目的語のゼロ代名詞が存在する場合
            if not Ob_Follow:
                self.logger.info('->Objectum_Follow!!')
                # 格フレームでどの格を補うか調べる
                if self.O_index != 0:
                    Ob_word = self.Ob_list[self.O_index - 1]
                    if Do_word != '' and Ob_word not in sentence and len(
                            Ob_word) != 0:
                        self.logger.info(
                            'Pair:(' + str(Ob_word) +
                            ' → ' + str(Do_word) + ')'
                        )
                        frame = self.SQ_usr.check(Do_word, Ob_word)
                        self.logger.info('frame->' + str(frame))

                        # 格助詞が判明した場合、目的語を補う
                        if frame != 0:
                            sentence = self.Follow_word(
                                sentence, Ob_word, fell_part, frame, Do_word_all, usr_id)

        self.logger.info('sentence->' + str(sentence))
        self.logger.info('----------Zero_Part_end----------')
        return sentence

    ##########################################################################

    ##########################################################################

    # 中心化理論により、話題の焦点を探す##########################
    def Centering(self, sentence, usr_id):
        self.logger.info('----------Centering_start----------')
        # 形態素解析を行う
        wakati, part = self.mecab_user.get_word_part_list(sentence)
        part = [y.split('-') for y in part]
        self.logger.info('Word_list->' + str(wakati))
        Cf = {}
        Cb_now = ''

        # すべての単語に対して
        particle_words = self.particle_dic.keys()
        for i, word in enumerate(wakati):
            word_thing = ''
            thing_flag = False
            word_class = part[i][0]
            pre_word = wakati[i - 1]
            pre_part = part[i - 1][0]

            # 特定の助詞が存在するか
            if word_class == '助詞' and word in particle_words:
                if '終助詞' not in part[i][1] and '接続助詞' not in part[i][1]:
                    # 補完する対象が助詞の場合は除く
                    if (
                        pre_word not in self.AVOID_WORD_LIST
                        and pre_part != '助詞'
                        and pre_part != '助動詞'
                    ):
                        # 「の、こと、もの」
                        if pre_word in self.FOLLOW_WORD_LIST:
                            thing_flag = True
                            # print('の、こと、もの')
                            word_thing = wakati[i - 2] + pre_word
                        # 「名詞+接尾」
                        elif part[i - 1][0] == '名詞' and part[i - 1][1] == '接尾':
                            word_thing = wakati[i - 2] + pre_word
                        # それ以外
                        else:
                            word_thing = pre_word

                        # サ変接続+「する」を結合
                        if (
                            self.mecab_user.get_original_word(
                                wakati[i - 2]) == 'する'
                            and thing_flag
                        ):
                            if part[i -
                                    3][0] == '名詞' and part[i -
                                                           3][1] == 'サ変接続':
                                # print('サ変接続+「する」')
                                word_thing = wakati[i - 3] + word_thing

                        # 「形容動詞語幹+助動詞」
                        elif (
                            wakati[i - 2] == 'な'
                            and part[i - 2][0] == '助動詞'
                            and thing_flag
                        ):
                            if part[i -
                                    3][0] == '名詞' and part[i -
                                                           3][1] == '形容動詞語幹':
                                # print('形容動詞語幹+助動詞')
                                word_thing = wakati[i - 3] + word_thing
                        # 動詞「った」
                        elif (
                            wakati[i - 2] == 'た'
                            and part[i - 2][0] == '助動詞'
                            and thing_flag
                        ):
                            if part[i -
                                    3][0] == '動詞' and part[i -
                                                           3][1] == '自立':
                                # print('動詞+自立')
                                word_thing = wakati[i - 3] + word_thing

                        # 助詞の直前の語をその助詞に対応付けて格納
                        if word_thing != '':
                            val = self.particle_dic[word]
                            Cf[word_thing] = val

        # ソートして、結果をリストとして出す
        Cf_sort = sorted(Cf.items(), key=lambda x: x[1])
        self.logger.info('Cf:' + str(Cf_sort))

        if len(Cf_sort) != 0:
            # ソートしていることにより、一番最初のリストのタプルがCpであるため代入
            Cp = Cf_sort[0][0]
            if 'あなた' in Cp or '私' in Cp:
                self.My_your = usr_id

            # Cp履歴のリストに追加
            self.Cp_list.append(Cp)
            Prev_Cp = self.Cp_list[- 1]
            self.logger.info('Cp:' + str(Prev_Cp))

            # Cbを求める
            # 前のCpがある場合、文の中にCpの単語があるかどうか確認
            if Prev_Cp != '':
                for word in wakati:
                    if word in Prev_Cp:
                        Cb_now = Prev_Cp
                if Cb_now == '':
                    Cb_now = Cp
                self.Cb_list.append(Cb_now)
                self.logger.info('Cb：' + str(self.Cb_list))

            # 状態遷移を求める
            if Cb_now == self.Cb_list[-1] or Cb_now == '':
                if Cb_now == Cp:
                    self.TRANSITION_list.append('CONTINUE')
                elif Cb_now != Cp:
                    self.TRANSITION_list.append('RETAIN')
            elif Cb_now != self.Cb_list[-1]:
                if Cb_now == Cp:
                    self.TRANSITION_list.append('SMOOTH-SHIFT')
                elif Cb_now != Cp:
                    self.TRANSITION_list.append('ROUGH-SHIFT')

            # 使用メモリ削減のためにCb_listとCp_listを上限20以下にする

            if len(self.Cb_list) > 20 and len(self.Cp_list) > 20:
                del self.Cb_list[0]
                del self.Cp_list[0]
                #self.index -= 1

            self.logger.info('TRAN：'+str(self.TRANSITION_list[-1]))
            #self.index += 1

        self.logger.info('----------Centering_end----------')

    #####################################################################

    # 目的語の先行詞を探す############################################
    def Objectum(self, sentence):
        self.logger.info('----------Objectum_start----------')

        # CaboChaによりかかり受けの関係を調べる
        word_list = self.Cabocha_user.get_chunks(sentence)
        len_word = len(word_list)

        # 述語にかかっている名詞が存在するか
        for i in range(len_word):
            # 名詞が主題ではない場合
            Fo1_word = word_list[i][0]
            Fo2_word = word_list[i][1]
            # 係り元と係り先の表示
            self.logger.info('Pair:(' + str(Fo1_word) +
                             ' → ' + str(Fo2_word) + ')')
            if len(self.Cp_list) != 0:
                if self.Cp_list[-1] not in Fo1_word:
                    # 形態素解析を行う
                    w_word, w_part = self.mecab_user.get_word_part_list(
                        Fo1_word)
                    w_part = [y.split('-') for y in w_part]
                    d_wakati, d_part = self.mecab_user.get_word_part_list(
                        Fo2_word)
                    d_part = [y.split('-')[0] for y in d_part]
                    # かかり先が述語であるかどうか
                    if '動詞' in d_part or '形容詞' in d_part or '助動詞' in d_part:
                        len_w_part = len(w_part)
                        for j in range(len_w_part):
                            # 名詞 + 助詞である場合
                            part = w_part[j][0]
                            p_part = w_part[j - 1][0]

                            if part == '助詞' and p_part == '名詞':
                                # 先行詞には用いない単語を探索
                                if (w_word[j - 1] not in self.AVOID_WORD_LIST and w_word[j - 1] not in self.Not_noun_words):
                                    Ob_word = ''
                                    # 「の、こと、もの」
                                    if w_word[j - 1] in self.FOLLOW_WORD_LIST:
                                        Ob_word = w_word[j - 2]

                                    # 「名詞+接尾」の場合は前の単語と統合する
                                    elif w_part[j - 1][1] == '接尾':
                                        if w_part[j - 2][0] == '名詞':
                                            Ob_word = w_word[j -
                                                             2] + w_word[j - 1]
                                    # それ以外はそのまま
                                    else:
                                        Ob_word = w_word[j - 1]

                                    self.Ob_list.append(Ob_word)
                                    self.logger.info(
                                        'OJ_list' + str(self.Ob_list))
                                    self.O_index += 1

        self.logger.info('----------Objectum_end----------')

    # ゼロ代名詞の補い############################################
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

    # 簡単な照応解析(中心化理論ver)##################################
    def anaphoric_analysis_Center(self, sentence):
        sentence = self.mecab_user.get_wakatied_sentence(sentence)
        word_list = sentence.split()
        next_word = ''
        # すべての単語に対して
        for i, word in enumerate(word_list):
            # 照応詞が存在するか
            if word in self.else_anaphor_words:
                # 単語の候補を選ぶ
                next_word = self.Category_check(word, self.Cb_list)

                # もしCbになければ、Obから選ぶ
                if next_word == '' and self.Ob_list != '':
                    next_word = self.Category_check(word, self.Ob_list)

                # 直接照応処理
                if next_word != '':
                    self.logger.info(word_list[i] + '->' + next_word)
                    word_list[i] = next_word
        # リストにしていた単語を文に再整形する
        sentence = ''
        for word in word_list:
            sentence += word
        return sentence

    # カテゴリを元に照応詞を補う候補を見つける####################
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
        # self.index = 0  # Cbのインデックス
        self.O_index = 0  # Obのインデックス

# Logger


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

    # 西村先生からの依頼に使ったもの
    # with open('QAuse.csv', 'r') as f:
    #     with open('result.csv', 'w') as wf:

    #         c = 0
    #         for line in f.readlines():
    #             c += 1
    #             if(c % 2 == 1):

    #                 # print('fromt'+line)
    #                 wf.write(Center.Centering_Word(
    #                     line.rstrip('\n'), 0) + '\n')
    #             else:
    #                 # print('next'+line)
    #                 wf.write(Center.Centering_Word(
    #                     line.rstrip('\n'), 1) + '\n')
    #                 Center.Forget_centering_element()


if __name__ == '__main__':
    main()
