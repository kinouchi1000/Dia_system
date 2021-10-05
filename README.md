# SpeechDialogSystem(対話システムの概要
作成者：木内

研究内容：[対話状況からの応答生成]
で使用した研究データをまとめています

このプログラムは一部2020年卒業の森雷太さんのプログラムを引用しています。
# 各ファイルについて

##README.md
  このファイル

##照応解析
- Centering_Theory.py
  書き言葉→話し言葉変換
  照応解析、ゼロ代名詞補完、ゼロ目的語補完

- example.db
  京都大学各フレームのDB
- xml_SQ.py
  京都大学各フレームDBのモデル

- talk2write.py
  Talk2Writeフォルダの中にある話し言葉→書き言葉変換モデルを呼び出す

- preprocessing.py
  対話システムの学習データを作成する

# 各フォルダについて

##  Talk2Write (talk to write)
名大対話コーパス(書き言葉に変換済み)をTransformerのT5-base-japaneseを使って
学習した後、書き言葉変換します。
"run finetune.sh"でファインチューンを行います。
 2021/07/28時点で一番いいのが、"output epoch1000"のモデルです。
inference.pyを実行すると対話形式で話し言葉を書き言葉に変換してくれます。

## ResponceGenerator
対話システムが存在します。

## nucc data
名大対話コーパスを格納しています。
