# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2025-10-24 14:52:20.975257
# @Last Modified by: CPS
# @Last Modified time: 2025-10-24 14:52:20.975257
# @file_path "W:\CPS\MyProject\projsect_persional\cps-scripts\src\pdf"
# @Filename "merge_pdf.py"
# @Description: 功能描述
#
import os, sys

sys.path.append("..")
sys.path.append("../..")

from os import path
from pathlib import Path
from pydantic import BaseModel
from pypdf import PdfWriter
import argparse

from utils import Utils
from typing import Optional


def merge_pdfs(pdf_list, output_pdf: str = None):
    merger = PdfWriter()

    for pdf in pdf_list:
        merger.append(pdf)

    if output_pdf is None:
        pdf_file = Path(pdf_list[0])
        output_pdf = str(pdf_file.resolve()).replace(pdf_file.suffix, "_merge.pdf")

    merger.write(output_pdf)
    merger.close()


class MergePdfConfigType(BaseModel):
    input_floder: str
    output_floder: Optional[str]
    output_name: Optional[str]


def configInit() -> MergePdfConfigType:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "input_floder",
        help="要转换的文件夹",
        type=str,
    )

    parser.add_argument(
        "--output_floder",
        help="要导出的文件夹，默认工作目录，采用目录名称.pdf",
        type=str,
        default=None,
    )

    parser.add_argument(
        "--output_name",
        help="输出的名称",
        type=str,
        default=None,
    )

    return parser.parse_args()


def main():
    config = configInit()

    input_dir = config.input_floder
    output_dir = config.output_floder if config.output_floder else input_dir
    output_name = config.output_name if config.output_name else f"{path.dirname(input_dir)}_merge.pdf"
    output_full_path = path.join(output_dir, output_name)

    file_list = Utils.get_file_list(input_dir, [".pdf"], True)
    if len(file_list) > 0:
        merge_pdfs(file_list, output_full_path)


def test():
    # 合并pdf
    # t = r"W:\CPS\MyProject\projsect_persional\电工高压证\高压电工1504题\pdf"

    # file_list = Utils.get_file_list(t, [".pdf"], True)

    # merge_pdfs(file_list)
    print("merge_pdf.py")


if __name__ == "__main__":
    if len(sys.argv) > 3:
        try:
            main()

        except Exception as e:
            print("【main】", str(e))
            Utils.delay(5)
        finally:
            exit()
    else:
        test()
