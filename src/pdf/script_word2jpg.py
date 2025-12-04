# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2025-12-02 16:27:08.960401
# @Last Modified by: CPS
# @Last Modified time: 2025-12-02 16:10:34.831469
# @file_path "W:\CPS\MyProject\projsect_persional\cps-scripts\src\pdf"
# @Filename "word2jpg.py"
# @Description: word文件导出jpg，先将文件转换成pdf到临时目录
#
import os, sys
from pathlib import Path
from os import path

sys.path.append("..")
from utils import Utils
import argparse
from pydantic import BaseModel

from word2pdf import convert_word_to_pdf
from pdf2img import pdf_to_A4_300dpi


# 单纯为了添加代码提示，需要手动与parser的变量同步更新
class ConfigType(BaseModel):
    input_file: str


def configInit() -> ConfigType:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "input_file",
        help="要转换的word文件，仅支持docx或者doc结尾的文件",
        type=str,
    )

    return parser.parse_args()


def main():
    config = configInit()

    targetFile = Path(config.input_file)

    if not targetFile.suffix.lower() in [".docx", ".doc"]:
        return print("不支持的格式文件: ", targetFile.stem)

    if not path.exists(targetFile):
        return print("不存在的文件: ", targetFile.stem)


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
