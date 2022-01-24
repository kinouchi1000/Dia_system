import readline
from Logger import Logger
from datetime import datetime
from logging import getLogger, StreamHandler, FileHandler, Formatter, DEBUG, WARN, INFO
from typing_extensions import ParamSpecArgs

from fairseq import checkpoint_utils, distributed_utils, options, tasks, utils
from fairseq.data import encoders
from fairseq.token_generation_constraints import pack_constraints, unpack_constraints
from fairseq_cli.generate import get_symbols_to_strip_from_output

from fairseq.dataclass.configs import FairseqConfig
from fairseq.dataclass.utils import convert_namespace_to_omegaconf


from Talk2Write.talk2write import talk2write  # 話し言葉→書き言葉
from TextCompletion.Centering_Theory import Centering_Theory  # 中心化理論
from JDTransformer.scripts.dialog import FavotModel, Favot  # 対話生成システム
# 対話生成(バージョン：nuccコーパスのみ)
# from ResponceGenerator.Gen_reference import Gen_reference


# 対話システムモデル
class DiaSystemModel:
    def __init__(self, logPath, parser, args, cfg):
        self.logPath = logPath
        self.parser = parser
        self.args = args
        self.cfg = cfg

        # log周り
        self.mainLogger = Logger.set_logger(
            "Dia_system", self.logPath + "Dia_system/")
        self.t2wLogger = Logger.set_logger(
            "Talk2Write", self.logPath + "Talk2Write/")
        self.centerLogger = Logger.set_logger(
            "Centering_Theory", self.logPath + "Centering_Theory/")
        self.diaLogger = Logger.set_logger("dialog", logPath + "dialog/")

        # Model
        self.talk2write = None
        self.Centering_Theory = None
        # 書き言葉変換
        if(args.use_talk2write_model):
            self.talk2write = talk2write(args, self.t2wLogger)
        # 中心化理論
        if(args.use_centering_method):
            self.Centering_Theory = Centering_Theory(self.centerLogger)
        # 応答生成
        fm = FavotModel(args, logger=self.diaLogger)
        self.favot = Favot(args, fm, logger=self.diaLogger, parser=parser)


class DiaSystem:

    # 初期化
    def __init__(self, dModel):
        self.dModel = dModel
        self.usr = 0

    # 対話生成

    def main(self, uttr, preUttr):

        # 入力ダイアログ
        uttr = uttr.strip()

        self.dModel.mainLogger.info("input_utterance:" + uttr)

        self.dModel.mainLogger.info("---------入力整形-----------")
        # uttr = self.inputFormat(uttr)           #　入力整形

        # 話し言葉→書き言葉変換
        if(self.dModel.talk2write != None):
            # 前回の対話
            preUttr = self.dModel.talk2write.translate_t2w(preUttr)
            self.dModel.mainLogger.info("SYS書き言葉変換:"+ preUttr)
            
            # 現在の対話
            uttr = self.dModel.talk2write.translate_t2w(uttr)
            self.dModel.mainLogger.info("USR書き言葉変換:" + uttr)


        # 文脈係り受け解析
        if(self.dModel.Centering_Theory != None):
            # 前の対話
            preUttr = self.dModel.Centering_Theory.Centering_Word(preUttr, 1)
            self.dModel.mainLogger.info("SYS照応解析:" + preUttr)
            # 現在の対話
            uttr = self.dModel.Centering_Theory.Centering_Word(uttr, 0)
            self.dModel.mainLogger.info("USR照応解析:" + uttr)

        # 応答生成
        self.dModel.mainLogger.info("---------応答分生成-----------")
        uttr = self.dModel.favot.execute(uttr)
        self.dModel.mainLogger.info("output_utterance:" + uttr[0])

        return uttr

    # 過去のデータリセット
    def dialogueReset(self):
        self.dModel.favot.reset()
        if(self.dModel.Centering_Theory != None):
            self.dModel.Centering_Theory.Forget_centering_element()
        self.dModel.mainLogger.info("----------対話内容---------------")

# APIのためにオブジェクト作成
# DialogueSystem = DiaSystem()


def add_local_args(parser):
    parser.add_argument('--max-contexts', type=int, default=4,
                        help='max length of used contexts')
    parser.add_argument('--suppress-duplicate', action="store_true",
                        default=False, help='suppress duplicate sentences')
    parser.add_argument('--show-nbest', default=3,
                        type=int, help='visible candidates')
    parser.add_argument(
        '--starting-phrase',
        default="こんにちは。よろしくお願いします。",
        type=str,
        help='starting phrase')
    parser.add_argument('--use-talk2write-model', action='store_true',
                        help='Use convertor talk-to-write model')
    parser.add_argument('--talk2write-model-dir', type=str,
                        help='Talk-to-Write model directory')
    parser.add_argument('--talk2write-tokenizer-dir', type=str,
                        help='Talk-to-Write tokenizer directory')
    parser.add_argument('--use-centering-method', action='store_true',
                        help='Use Centering Method for Contextual resolution')
    return parser


def main():
    # Get parameter
    parser = options.get_interactive_generation_parser()
    add_local_args(parser)
    args = options.parse_args_and_arch(parser)
    cfg = convert_namespace_to_omegaconf(args)

    # 対話システム用Model
    logPath = "Data/Log/"
    diaSystemModel = DiaSystemModel(logPath, parser, args, cfg)
    diaSystem = DiaSystem(diaSystemModel)
    output = diaSystemModel.favot.execute("||init||")[0]
    print(output)
    turnCount = 0  # debug用
    while True:

        text = input("USR:")
        if text.startswith("/reset"):
            diaSystem.dialogueReset()
            output = diaSystemModel.favot.execute("||init||")[0]
            print("success to reset!!")
            turnCount = 0
            continue
        output = diaSystem.main(text, output)
        if output is None or len(output) != 2:
            continue
        output, output_debug = output
        if output is not None:
            diaSystemModel.diaLogger.info("sys_uttr:" + output)
            print("\n".join(output_debug))
            print("SYS:" + output)

            # debug
            turnCount += 2
            print(str(turnCount))


if __name__ == "__main__":
    main()
