#!/usr/bin/env python
# -*- coding: utf-8 -*-

import CaboCha

# CaboChaを使うためのクラス
class Cabocha:
    # 各種ユーザー
    Cabocha= None
     # 形態素解析用の辞書の場所
    MECAB_NEOLOGD_DIC_PATH = '/home/kinouchitakahiro/anaconda3/envs/DSTS/lib/mecab/dic/mecab-ipadic-neologd'

     # 解析器を用意
    def __init__(self):
        self.Cabocha = CaboCha.Parser("-d" + self.MECAB_NEOLOGD_DIC_PATH)

    def get_chunks(self,sentence):
        tree =  self.Cabocha.parse(sentence)
        # 形態素を結合しつつ[{c:文節, to:係り先id}]の形に変換する
        word_list=[]
        chunks = []
        text = ""
        toChunkId = -1
        for i in range(0, tree.size()):
            token = tree.token(i)
            text = token.surface if token.chunk else (text + token.surface) 
            toChunkId = token.chunk.link if token.chunk else toChunkId
            # 文末かchunk内の最後の要素のタイミングで出力
            if i == tree.size() - 1 or tree.token(i+1).chunk:
                chunks.append({'c': text, 'to': toChunkId})

        # 係り元→係り先の形式で出力する
        for chunk in chunks:
            if chunk['to'] >= 0:
                tuple1=(chunk['c'],chunks[chunk['to']]['c'])
                word_list.append(tuple1)      
        return word_list
    
if __name__=='__main__':
    cabo=Cabocha()
    sentence=input('input:')
    word_list=cabo.get_chunks(sentence)
    print(word_list)
