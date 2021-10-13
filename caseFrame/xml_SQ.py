#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SQLite3より、「京都大学格フレーム」元にデータベースを作成し、格助詞を検索するクラス
"""
import memory_profiler
import sqlite3
import xml.etree.ElementTree as ET
import time


class XML_SQ:
    conn = None
    c = None
    # 格助詞の変換
    particle_dic = {
        "ガ格": "が",
        "ニ格": "に",
        "ノ格": "の",
        "ヘ格": "へ",
        "ヲ格": "を",
        "ト格": "と",
        "デ格": "で",
        "カラ格": "から",
        "マデ格": "まで",
        "ヨリ格": "より",
    }

    def __init__(self, DBFile):
        # データベースに接続する
        self.conn = sqlite3.connect(DBFile)
        self.c = self.conn.cursor()

    # 「京都大学格フレーム」用のデータベースを新たに作成する############################
    def read_xml_serially(self, file_path):

        # テーブルの作成
        self.c.execute(
            """CREATE TABLE users(word text,frame text,Main text,score integer)"""
        )
        frame = ""
        # xmlファイルを解析
        ite = ET.iterparse(file_path, events=("start", "end"))
        for elem in ite:
            # 述語の決定
            if elem.tag == "entry":
                if elem.attrib != {}:
                    Do_word = elem.attrib["headword"]
            # 格助詞の決定
            elif elem.tag == "argument":
                if elem.attrib != {}:
                    if (
                        elem.attrib["case"] in self.particle_dic
                        and "~" not in elem.attrib["case"]
                    ):
                        frame = self.particle_dic[elem.attrib["case"]]
                    else:
                        frame = ""
            # 目的語の決定
            elif elem.tag == "component":
                if elem.attrib != {}:
                    frequency = elem.attrib["frequency"]
                    Main_word = elem.text
                else:
                    if frame != "":
                        # データの挿入
                        sql = "INSERT INTO users VALUES (?,?,?,?)"
                        usr = (Do_word, frame, Main_word, frequency)
                        self.c.execute(sql, usr)
            elem.clear()

        # 挿入した結果を保存（コミット）する
        self.conn.commit()

        # データベースへのアクセスが終わったら close する
        self.conn.close()

    # データベースから格助詞の検索を行う########################################################
    def check(self, Do_word, Main_word):
        t1 = time.time()
        # 述語と目的語の探索
        sql = "SELECT * FROM users WHERE word like ? and Main like ?  LIMIT 5;"
        frame_list = [row for row in self.c.execute(sql, (Do_word + "%", Main_word))]
        # 格フレームが発見した場合
        if frame_list != []:
            # frequencyが高い順にソート
            frame_list = sorted(frame_list, key=lambda frame: frame[3], reverse=True)
            # print(frame_list[0])
            frame = frame_list[0][1]
        else:
            frame = 0

        # 経過時間の出力
        t2 = time.time()
        elapsed_time = t2 - t1
        print(f"DB検索経過時間：{elapsed_time}")
        return frame

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    xml_sq = XML_SQ("caseFrame/example.db")
    XML_read = False

    # Trueであれば，DBの作成を行う
    if XML_read == True:
        file_path = "kyoto-univ-web-cf-2.0/kyoto-univ-web-cf-2.0.xml"
        xml_sq.read_xml_serially(file_path)
    # Falseの場合，DBの検索を行う
    else:
        while 1:
            try:
                Main_word = input("input:")
                Do_word = input("input:")
                frame = xml_sq.check(Do_word, Main_word)
                print(frame)
            except KeyboardInterrupt:
                print("input_KeyError")
                xml_sq.close()
                break
            except:
                pass
