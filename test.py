# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2025-10-24 14:52:20.975257
# @Last Modified by: CPS
# @Last Modified time: 2025-10-24 14:52:20.975257
# @file_path "W:\CPS\MyProject\projsect_persional\cps-scripts\src"
# @Filename "test.py"
# @Description: 功能描述
#
import os, sys

sys.path.append("..")

from os import path
from pathlib import Path
from pydantic import BaseModel

import argparse
from src.utils import Utils
from typing import Any, Optional


class ArgsType(BaseModel):
    action: Any


def configInit() -> ArgsType:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "target",
        help="右键选择的东西",
        type=str,
    )

    return parser.parse_args()


import time

if __name__ == "__main__":
    print(111111111111111111)

    for each in sys.argv:
        print(each)

    time.sleep(10)

    # try:
    #     config = configInit()

    #     Utils.exitWithMsg(config.target)
    # except Exception as e:
    #     print("错误: ", str(e))
    #     import time

    #     time.sleep(10)
    #     exit()
