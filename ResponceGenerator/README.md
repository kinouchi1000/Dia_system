# 
## output
[finetuningの例]{https://note.com/npaka/n/n8a435f0c8f69}の例の通り学習させてみた結果
あまりうまくいってない．
学習epochは3
```
USR: 今日の実験はいかがでした？
こんにちわ こんにちわ いや、***いいですか、***。 あ、すいません、すいません。 いや、***いいですか、*** 。 今日の実験はいかがでした?
```

## output_3_1
以下のように過去の履歴を3つと，1つを合わせて学習させたもの
```
こんにちは_今日はいい天気ですね_そうですね</s>ご飯は食べました？
```
また，学習エポックは100で指定



## REQUIREMENTS
name | 2021/8/24 | colab | 入れた 
tensorboard		False	T	*
scikit-learn		False	T	*
seqeval			False	False
psutil			False	T	*
sacrebleu >= 1.4.12	T	False
rouge-score		False	False
tensorflow_datasets	False	T	*
matplotlib		False	T	*
git-python==1.0.3	False	False
faiss-cpu		False	False
streamlit		False	False
elasticsearch		False	False
nltk			False	T	*
pandas			T	False
datasets >= 1.1.3	T	False
fire			False	False
pytest			False	T	*
conllu			False	False
sentencepiece != 0.1.92	T	False
protobuf		T	False

