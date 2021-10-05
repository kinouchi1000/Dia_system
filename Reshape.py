#!/usr/bin/env python
# coding:utf-8

'''
Centering_Theoryを利用して学習データを整形する
'''
import sys
import re
from Centering_Theory import Centering_Theory

class reshape:

    # ユーザーの定義
    wf = None
    centering_theory = None
    
    # 初期化
    def __init__(self, wfname):
        self.centering_theory = Centering_Theory()
        try:
           self.wf = open(wfname,'w',encoding = 'UTF-8')
        except OSError as e:
            print(e)
            sys.exit()
    
    # 書き込みファイルを閉じる
    def close(self):
        self.wf.close()
    ''' 
    ファイル整形
    [除くもの]
    - ＠が先頭につくもの
    -　カッコなどがつくもの
    '''
    def reshapeData(self,filename):
        #中心化理論の初期化
        self.centering_theory.Forget_centering_element()
        # 中心化理論のユーザ
        usr = 0
        try: 
            f = open(filename, 'r')
        except OSError as e:
            print(e)
            return True
        else:
            try:
                print(filename+"：整形開始")
                line = f.readline()
                while line:
                    # 改行削除
                    line = line.strip()
                    # 整形処理
                    top_pattern = re.match('^＠',line)
                    if(top_pattern):
                        line = f.readline()
                        continue
                    line = re.sub(r'.*：','',line)
                    line = re.sub(r'（.*?）','',line)
                    line = re.sub(r'＜.*?＞','',line)
                    line = re.sub(r'【.*?】','',line)
                    # 空行の場合飛ばす
                    if(line == ""):
                        line=f.readline()
                        continue
                    
                    #中心化理論で整形
                    line = self.centering_theory.Centering_Word(line,usr)
                    
                    # ファイル書き込み
                    self.wf.write(line+"\n")
                    line = f.readline()
                self.wf.write("[EOD]\n")
            except Exception as e:
                print(e)
                return True
            finally:
                f.close()
                return False


if __name__ == "__main__":
    
    index = 0
    # ファイル読み込み終了フラグ
    flg = False
    reshape = reshape("ResponceGenerator_t2w/clean.txt")
    while index<130:
    
        index+=1
        filename ="nucc/data{:03d}.txt".format(index)
        flg = reshape.reshapeData(filename)
        if flg == True:
            reshape.close()
            break
    print("ファイル整形終了")
