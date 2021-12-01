#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ログやコマンドライン表示用のクラス
"""
import readline
from datetime import datetime
from logging import getLogger, StreamHandler, FileHandler, Formatter, DEBUG, WARN, INFO


class Logger():
    # Logger
    def set_logger(name, dirname="log/main/"):
        dt_now = datetime.now()
        dt = dt_now.strftime('%Y%m%d_%H%M%S')
        fname = dirname + dt
        logger = getLogger(name)
        #handler1 = StreamHandler()
        #handler1.setFormatter(Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
        handler2 = FileHandler(filename=fname)
        handler2.setLevel(DEBUG)  # handler2はLevel.WARN以上
        handler2.setFormatter(
            Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
        # logger.addHandler(handler1)
        logger.addHandler(handler2)
        return logger
