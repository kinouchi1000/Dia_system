#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

# すべての対話データを結合
cat ./nucc/*.txt > nucc_all.txt



cat nucc_all.txt | 
    perl -pe 's/^＠ＥＮＤ.*/[EOD]/g'|\
    perl -pe 's/＠.*\n//g' |\
    perl -pe 's/.*：//g' |\
    perl -pe 's/（.*?）//g' |\
    perl -pe 's/＜.*?＞//g' |\
    perl -pe 's/【.*?】//g' |\
    perl -pe 's/　\n//g'|\
    grep . > nucc_all.clean.txt 

# NOTE:過去の履歴三つの場合
cat nucc_all.clean.txt |\
	perl -ne 'BEGIN{$p3="";$p2="";$p1=""} chomp; if($.>3 && $_ ne "[EOD]" && $p1 ne "[EOD]" && $p2 ne "[EOD]" && $p3 ne "[EOD]"){print $p3 . "[SEP]" . $p2 . "[SEP]" . $p1 . "</s>" . $_ . "\n";} $p3=$p2; $p2=$p1; $p1=$_;' > nucc.train.txt

# NOTE: 過去の履歴一つの場合
cat nucc_all.clean.txt |\
	perl -ne 'BEGIN{$p=""} chomp;  if($.>1 && $_ ne "[EOD]"&&$p ne "[EOD]"){print $p . "</s>" . $_ . "\n";} $p=$_;' >> nucc.train.txt

#validation用のデータ作成

shuf nucc.train.txt | head -n 6000 > nucc.validation.txt
