# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2025-10-23 08:29:39.457065
# @Last Modified by: CPS
# @Last Modified time: 2025-10-23 08:29:39.457065
# @file_path "W:\CPS\MyProject\projsect_persional\cps-scripts\src"
# @Filename "test.py"
# @Description: 将指定的目录下文件打包成单个pdf，目前仅支持jpg、jpeg
#
import os, sys
from os import path

sys.path.append("..")
sys.path.append("../..")

from pathlib import Path
from pydantic import BaseModel
from utils import Utils

import argparse
import img2pdf


def get_file_list(target_dir: str, suffixes: list[str]) -> list[str]:
    file_list = [str(path) for pattern in suffixes for path in Path(target_dir).glob(pattern)]
    return file_list


# 单纯为了添加代码提示，需要手动与parser的变量同步更新
class ConfigType(BaseModel):
    input_floder: str


def configInit() -> ConfigType:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "input_floder",
        help="要转换的文件夹",
        type=str,
    )

    parser.add_argument(
        "--output_floder",
        help="要导出的文件夹，默认工作目录",
        type=str,
        default=None,
    )

    return parser.parse_args()


def main():
    config = configInit()

    if not config.input_floder:
        Utils.exitWithMsg("指定一个文件夹")

    # 注册表右键作用在目录背景上时，无法传参，使用固定参数
    if config.input_floder == "USE_CWD":
        config.input_floder = os.getcwd()
        output_pdf = os.getcwd()

    target_Path = Path(config.input_floder)
    if target_Path.is_file():
        Utils.exitWithMsg("仅支持文件夹")

    if not config.output_floder:
        config.output_floder = os.getcwd()

    # 默认在工作目录生成
    output_pdf = path.join(config.output_floder, f"{target_Path.name}.pdf")

    suffixes = ["*.jpg", "*.jpeg", "*.png"]
    file_list = get_file_list(config.input_floder, suffixes)
    if len(file_list) == 0:
        Utils.exitWithMsg(f"文件夹中没有任何{'|'.join(suffixes)}文件")

    print(f"本次处理图片: {len(file_list)}张\n")
    # 创建封面
    with open(output_pdf, "wb") as pdf_file:
        pdf_file.write(img2pdf.convert(file_list))

    Utils.exitWithMsg(f"合并完成: {output_pdf}\n\n本窗口10秒自动关闭")


def test():
    config = configInit()

    print("config: ", config.input_floder)


# 计算机\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\CpsPDF\command
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
