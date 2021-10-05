use strict;
use utf8;
use open qw/ :utf8 :std /;

#明大コーパスのデータ整形

while(my $str = <> ){
	#(1)確認済みの行のみを抽出
	#(2)文が空欄の場合は除外
	#(3)xが含まれる場合は除外
	#JSON形式に整形
	#学習データと検証データに分割
	chomp $str;
	#(2)チェック
	if($str =~/(.*),(.*),(.*)/){
		#(1),(3)チェック
		if("$1"ne"確認" and "$1"ne"問題あり" and "$2"ne"" and "$3"ne"" and  "$2" !~ m/x/ and "$3" !~ m/x/){
			print "{ \"translation\": { \"wr\": \"$2\", \"sp\": \"$3\" } }\n"	
		}
	}	
}
