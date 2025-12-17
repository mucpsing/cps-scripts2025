# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2025-10-24 10:21:41.717528
# @Last Modified by: CPS
# @Last Modified time: 2025-10-24 10:21:41.717528
# @file_path "W:\CPS\MyProject\projsect_persional\cps-scripts\src"
# @Filename "utils.py"
# @Description: 工具函数
#
import os, sys

sys.path.append("..")

import time

from pathlib import Path
from PIL import Image, ImageFilter
from typing import Union, List
import fitz


def insert_blank_pages_after_each(input_pdf: str, output_pdf: str):
    """对一些只能双面打印的打印机，将PDF逐页插入空白页，可以达到单面打印的效果"""

    # 打开原始PDF
    doc = fitz.open(input_pdf)

    # 创建新的PDF文档
    # fitz原则上每次仅进行读或者写操作，这里创建一个空实例是为了将写操作更好的独立出来处理
    new_doc = fitz.open()

    # 遍历每一页
    for page_num in range(len(doc)):
        # 添加原始页面
        new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

        # 创建空白页（与原始页面相同尺寸）
        original_page = doc[page_num]
        new_doc.new_page(-1, width=original_page.rect.width, height=original_page.rect.height)

    # 保存新文档
    new_doc.save(output_pdf)
    doc.close()
    new_doc.close()


class Utils:
    @staticmethod
    def sharpen_image(input_path: str, output_path: str = None, factor=1.0):
        """
        对图片进行锐化处理并保存

        参数:
            input_path: 输入图片路径
            output_path: 输出图片路径（None表示原地保存）
            factor: 锐化强度（0.0到2.0之间，1.0为默认值）
        """
        # 打开图片
        with Image.open(input_path) as img:
            # 应用锐化滤镜
            times = max(1, int(factor * 1.5))  # 经验公式调整强度
            for _ in range(times):
                img = img.filter(ImageFilter.SHARPEN)

            # 确定输出路径
            save_path = output_path if output_path else input_path

            # 保存图片（原地保存时使用与原文件相同的格式）
            img.save(save_path, format=img.format if img.format else None)

    @staticmethod
    def get_file_list(target_dir: Union[str, Path], suffixes: List[str], deep: bool = False) -> List[str]:
        """
        获取指定目录下指定后缀的文件列表（支持递归）

        参数:
            target_dir: 目标目录路径
            suffixes: 文件后缀列表（如 ['.jpg', '.png']）
            deep: 是否递归搜索子目录（默认False）

        返回:
            文件绝对路径列表（已排序）
        """
        # 确保输入是Path对象
        file_list = []
        target_path = Path(target_dir).resolve()

        # 规范化后缀格式（确保以点开头，小写）
        normalized_suffixes = {f".{s.lstrip('.').lower()}" for s in suffixes}

        # 选择遍历方法
        if deep:
            # 递归遍历所有文件
            all_files = target_path.rglob("*")
        else:
            # 仅当前目录
            all_files = target_path.glob("*")

        # 筛选符合条件的文件
        file_list += [
            str(file.resolve()) for file in all_files if file.is_file() and file.suffix.lower() in normalized_suffixes
        ]

        # 按文件名自然排序
        return sorted(
            file_list,
            key=lambda x: [int(c) if c.isdigit() else c for c in os.path.splitext(os.path.basename(x))[0].split()],
        )

    @staticmethod
    def delay(sec: int):
        time.sleep(sec)

    @staticmethod
    def exitWithMsg(*msg: str):
        print(*msg)
        time.sleep(10)
        exit()


if __name__ == "__main__":
    tar = r"Z:\work\2025\项目\海南省水文“十五五”建设规划\请款\第三笔\报告\第三笔发票+封面盖章.pdf"
    out = r"Z:\work\2025\项目\海南省水文“十五五”建设规划\请款\第三笔\报告\第三笔发票+封面盖章_双面打印.pdf"
    insert_blank_pages_after_each(tar, out)
