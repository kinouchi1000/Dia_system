from Talk2Write.talk2write import talk2write  # 話し言葉→書き言葉
from Centering_Theory import Centering_Theory  # 中心化理論
from ResponceGenerator.Gen_reference import Gen_reference  # 対話生成(バージョン：nuccコーパスのみ)
from Wrapper.Treat_log import Logger


class Dia_system:
    # ユーザ
    talk2write = None
    Centering_Theory = None
    Gen_reference = None
    logger = None
    SYS = ""
    preUser = ""

    usr = 0

    # 初期化
    def __init__(self):
        # ユーザの設定
        T2W_model = "./Talk2Write/prefines/output_megagonalbs2"
        GenRef_model = "./ResponceGenerator/output_prefine/output_sameDialogerConnect"
        self.talk2write = talk2write(T2W_model, T2W_model)
        self.Centering_Theory = Centering_Theory()
        self.Gen_reference = Gen_reference(GenRef_model, GenRef_model)
        self.logger = Logger(self.__class__.__name__)  # ログ保存用
        # ユーザナンバー
        self.usr = 0

    # 対話生成
    def main(self, line, preUser=None, SYS=None):
        if preUser != None:
            self.preUser = preUser
        if SYS != None:
            self.SYS = SYS
        # 入力ダイアログ
        text = line.strip()
        self.logger.add_print_log("入力文:" + text)

        ###データ整形部###############
        self.logger.add_print_log("----------入力文整形----------")

        # 話し言葉→書き言葉変換
        text = self.talk2write.translate_t2w(text)
        self.logger.add_print_log("書き言葉変換:" + text)
        # print("( %.5f [sec] )" % (time_length))

        # 文脈係り受け解析
        text = self.Centering_Theory.Centering_Word(text, self.usr)
        self.logger.add_print_log("文脈照応解析：" + text)

        ###応答分生成################
        self.logger.add_print_log("---------応答分生成-----------")

        # 機械学習による応答分生成
        output, time = self.Gen_reference.Generate(text, self.preUser, self.SYS)
        self.logger.add_print_log("応答文:" + output)

        ###過去のダイアログの保存#####
        self.preUser = text
        self.SYS = output

        return output

    ## 過去のデータリセット
    def dialogueReset(self):
        self.SYS = ""
        self.preUser = ""


# APIのためにオブジェクト作成
DialogueSystem = Dia_system()

if __name__ == "__main__":
    Dia = Dia_system()
    while True:
        Input = input("USR:")
        Output = Dia.main(Input)
        print("SYS:" + Output)
