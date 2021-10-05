import time
import sys
import re
from transformers import T5Tokenizer, AutoModelForCausalLM



class Gen_reference:
    # ユーザ
    tokenizer = None
    model = None
    
    #初期化
    def __init__(self,model_name,tokenizer_name):
        #ユーザの設定
        self.tokenizer = T5Tokenizer.from_pretrained(tokenizer_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    # 次の対話文を生成する。
    def Generate(self,text,preUser="",SYS=""):
        
        # 入力データ整形
        text = text.rstrip()
        text = text.replace("？", "?")
        if(preUser == "" or SYS == ""):
            input_text = text
        else:
            input_text = preUser+"[SEP]"+SYS+"[SEP]"+text

        start = time.time()

        # 推論
        input_token = self.tokenizer.encode(input_text, return_tensors="pt")

        while True:
            result = self.model.generate(input_token, do_sample=True, max_length=100, pad_token_id=self.tokenizer.eos_token_id)#, max_time=1.0)
            output = self.tokenizer.batch_decode(result)[0]
        
            # 出力データ整形
            pattern = re.compile(input_text.replace("?", "\?"))
            #output = pattern.sub('', output)
            output = re.sub(r"^.*</s> ", "", output)
            #output = output.replace("?", "\?")
            output = output.replace("</s>", '')
            output = output.replace("<unk> ", '')
            output = output.replace("<|endoftext|>", '')
            
            if("[SEP]" not in output):
                break

        time_length = (time.time() - start)

        #後に対話履歴を残す
        preUser = text
        SYS = output
        return output, time_length

if __name__ == "__main__":
    Gen = Gen_reference("./output_prefine/output_sameDialogerConnect","./output_prefine/output_sameDialogerConnect/")
    while True:
        
        dia = input("USR:")
        SYS, TIME = Gen.Generate(dia)
        print("SYS:"+SYS,end = "")
        print("( %.5f [sec] )" % (TIME))
