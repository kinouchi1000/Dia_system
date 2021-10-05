# Dia_System

"Dia_System"とは、研究内容：[対話状況からの応答生成]で作成した対話システムAPIです
* このプログラムは一部2020年卒業の森雷太さんのプログラムを引用しています。

# API route

### /api/Dialogue/<int:user_id>
- GET
現在の対話のすべてのデータを取得
- POST
{data:{"sentence" : ""}}
対話をすすめる

### /api/Dialogue/<int:user_id>/start
- POST
”こんにちは”が格納されて、対話が始まる

### /api/User
- POST
　data: name　が存在しなければユーザデータ作成して、データを返す
なければ作ってデータを返す

# Requirement


# Quick Start
## apiを実行する場合
'''bash
nwsgi --ini init.ini
'''
## Dialogue Systemだけを実行する場合
'''bash
// 必要なら仮想環境に入る、計算機の環境名はDSTS
conda activate DSTS
python Dia_system.py
'''
# ファイル構成

## Centering__Theory.py
	照応解析、ゼロ代名詞補完、ゼロ目的語補完

## Dia_system.py
	対話システムのおおもと
	書き言葉変換→文脈照応解析→文章生成を行う

## main.py


## myapp.ini
uWSGIの設定ファイル

# ディレクトリ構成

## caseFrame
京都大学の各フレームのDBのラッパ

## Talk2Write
書き言葉話し言葉変換




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
