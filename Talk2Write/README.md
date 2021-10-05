# その後実行したコマンド
```
$ shuf --random-source=./data/nucc_spoken2written_20210709.txt nucc_spoken2written_20210709.json > nucc_spoken2written_20210
709.shuf.json
$ head -n 10000 nucc_spoken2written_20210709.shuf.json > nucc_spoken2written_20210709.train.json
$ tail -n 1437  nucc_spoken2written_20210709.shuf.json > nucc_spoken2written_20210709.valid.json
```

conda 4.10.3
python  3.8.10

# 使用しているpythonモジュール
pytorch 1.9.0 

transformers 4.4.2 (HuggingFace) 
datasets==1.9.1 (HuggingFace)
sentencepiece == 0.1.95

sacrebleu 1.5.1


#ファインチューニングコマンド
```terminal
python transformers/examples/seq2seq/run_translation.py --model_name_or_path sonoisa/t5-base-japanese --do_train --do_eval  --do_predict --source_lang sp --target_lang wr --train_file nucc_spoken2written_20210709.train.json --validation_file nucc_spoken2written_20210709.valid.json --test_file nucc_spoken2written_20210709.valid.json  --output_dir ./output --per_device_train_batch_size=4 --per_device_eval_batch_size=4 --overwrite_output_dir --predict_with_generate --max_train_samples 500 --max_val_samples 500 --num_train_epochs 10
```
