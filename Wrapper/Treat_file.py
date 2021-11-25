#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ファイルを扱うためのクラス
"""
import re


class File:
    def litch_load(self, path):
        """
        汎用性の高いファイルの読み込みフォーマット
        '#':コメントとして無視する
        '@':":"で区切られた単語を置換する @%話し手% : 私,わたし,俺,おれ,僕,ぼく
        "%":"@"の置換を適応する文字列 @%話し手%
        "_":"@"の属性を示す @%返事_肯定_%
        """
        data = []
        substitution_list = []
        box = open(path, 'r', encoding='utf-8')  # とりあえず全部取得

        # 処理
        for line in box:
            line = re.sub('\n', '', line)
            if line[0] == '@':  # '@'は設定用の文字
                # 置換用のリストを作成
                sub_line = line.split(':')
                sub_line[0] = re.sub('@', '', sub_line[0])
                substitution_list.append(sub_line)
            elif line[0] != '#':  # コメントアウトとして処理
                # 置換対象としてリストに格納
                data.append(line)
        box.close()

        # 置換を適応したデータを生成
        for i, line in enumerate(data):
            for sub_list in substitution_list:
                line = re.sub(sub_list[0], sub_list[1], line)
                data[i] = line

        return data

    # リストを指定のファイルに書き込む
    def write_list(self, path, list):
        file = open(path, 'w')
        for line in list:
            file.writelines(line)
        file.close()


if __name__ == "__main__":
    user = File()
    print(user.litch_load('./wrapper/hoge.txt'))
