# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2025-12-02 17:04:22.595720
# @Last Modified by: CPS
# @Last Modified time: 2025-12-02 17:04:22.595720
# @file_path "W:\CPS\MyProject\projsect_persional\cps-scripts\src\scripts"
# @Filename "pdf2jpg.py"
# @Description: 将pdf转换成A4 300DPI的jpg文件到同目录下
#
import os, sys

sys.path.append("..")

from os import path
from pathlib import Path
from pydantic import BaseModel
from pdf2img import pdf_to_A4_300dpi
from utils import Utils

import argparse


# 单纯为了添加代码提示，需要手动与parser的变量同步更新
class ConfigType(BaseModel):
    input_file: str


def configInit() -> ConfigType:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "input_file",
        help="要转换的pdf文件，仅支持docx或者doc结尾的文件",
        type=str,
    )

    return parser.parse_args()


def main():
    config = configInit()

    targetFile = Path(config.input_file)
    print("targetFile: ", targetFile)

    if not targetFile.suffix.lower() in [".pdf"]:
        return print("不支持的格式文件: ", targetFile.stem)

    if not path.exists(targetFile):
        return print("不存在的文件: ", targetFile.stem)

    output_path = path.dirname(config.input_file)

    pdf_to_A4_300dpi(config.input_file, output_path)


def test():
    pass


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            main()

        except Exception as e:
            print("【main】", str(e))
            Utils.delay(5)
        finally:
            exit()
    else:
        test()
