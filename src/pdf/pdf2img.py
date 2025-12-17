# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date:
# @Last Modified by: CPS
# @Last Modified time: 2025-12-02 16:10:34.831469
# @file_path "W:\CPS\MyProject\projsect_persional\cps-scripts\src\pdf"
# @Filename "pdf2img.py"
# @Description: 将pdf导出成300DPI的A4尺寸文件，这个格式与使用adobe DC中的导出JPG一直
#

import sys


sys.path.append("..")

from os import path
from pathlib import Path
from PIL import Image
from enum import Enum
import fitz, io
from pydantic import BaseModel
from typing import Optional, Dict, List


class PageOrientation(Enum):
    PORTRAIT = "portrait"  # 纵向
    LANDSCAPE = "landscape"  # 横向


class PageInfo(BaseModel):
    """页面信息模型"""

    page_number: int  # 页面序号（从0开始）
    original_width: float  # 原始宽度（点）
    original_height: float  # 原始高度（点）
    orientation: PageOrientation  # 页面方向
    is_landscape: bool  # 是否为横向（方便判断）


class Utils:
    @staticmethod
    def is_color_image(image, threshold=5):
        """
        检查图片是否包含明显的彩色元素

        Args:
            image: PIL Image对象
            threshold: 彩色判断阈值，值越小判断越严格

        Returns:
            bool: True表示包含彩色，False表示灰度图
        """
        if image.mode == "L":
            return False

        # 转换为RGB模式确保一致性
        if image.mode != "RGB":
            rgb_image = image.convert("RGB")
        else:
            rgb_image = image

        # 检查图片尺寸，如果太大则进行缩略以提高检查速度
        width, height = rgb_image.size
        if width * height > 1000000:  # 如果图片超过100万像素
            check_image = rgb_image.resize((100, 100), Image.Resampling.LANCZOS)
        else:
            check_image = rgb_image

        # 检查每个像素的RGB通道差异
        pixels = list(check_image.getdata())

        for r, g, b in pixels:
            # 如果RGB三个通道的值差异超过阈值，则认为有彩色
            if abs(r - g) > threshold or abs(g - b) > threshold or abs(r - b) > threshold:
                return True

        return False


def pdf_to_A4_300dpi(pdf_path, output_path, dpi=300, paper_size="A4"):
    basename = Path(pdf_path).stem

    # 定义A4和A3的尺寸（毫米）并转换为像素
    paper_sizes = {"A4": (210, 297), "A3": (297, 420)}
    width_mm, height_mm = paper_sizes.get(paper_size, ("A4"))

    # 毫米转英寸再乘以DPI
    # target_width = int(width_mm / 25.4 * dpi)
    # target_height = int(height_mm / 25.4 * dpi)

    # 毫米转英寸再乘以DPI
    portrait_width = int(width_mm / 25.4 * dpi)  # 纵向宽度
    portrait_height = int(height_mm / 25.4 * dpi)  # 纵向高度

    # 打开PDF并获取页面
    doc = fitz.open(pdf_path)
    for page in doc:
        original_width = page.rect.width  # 原始宽度（点）
        original_height = page.rect.height  # 原始高度（点）
        is_landscape = original_width > original_height
        # 根据方向确定目标尺寸
        if is_landscape:
            # 横向页面：交换A4的宽高
            target_width = portrait_height
            target_height = portrait_width
        else:
            # 纵向页面：使用标准A4尺寸
            target_width = portrait_width
            target_height = portrait_height

        # 计算适应目标尺寸的缩放比例
        scale_w = target_width / original_width
        scale_h = target_height / original_height
        scale = min(scale_w, scale_h)  # 保持宽高比

        # 生成缩放后的图像
        matrix = fitz.Matrix(scale, scale)
        pix = page.get_pixmap(matrix=matrix, dpi=dpi)

        img = Image.open(io.BytesIO(pix.tobytes()))
        img_mode = "RGB"
        img_bg_color = (255, 255, 255)
        if not Utils.is_color_image(img):
            img.convert("L")
            img_mode = "L"
            img_bg_color = 255

        # 创建目标尺寸画布并居中粘贴
        canvas = Image.new(img_mode, (target_width, target_height), img_bg_color)
        x = (target_width - img.width) // 2
        y = (target_height - img.height) // 2
        canvas.paste(img, (x, y))

        # 保存结果
        canvas.info["dpi"] = (dpi, dpi)  # 写入DPI信息

        if not isinstance(page.number, int):
            return print("pdf页码读取异常: ", len(doc))

        if page.number < 9:
            pageIndex = f"0{page.number + 1}"
        else:
            pageIndex = page.number + 1

        each_output_file = path.join(output_path, f"{basename}_{pageIndex}.jpg")

        canvas.save(each_output_file, "JPEG", quality=80, dpi=(dpi, dpi))

    doc.close()


if __name__ == "__main__":
    tar = path.abspath(r"Z:\work\2025\项目\海南省水文“十五五”建设规划\合同\扫描-海南省水文“十五五”建设规划报告编制项目技术咨询合同合同盖章扫描件（含订立审签单）.pdf")

    # print(Path(tar).stem)
    pdf_to_A4_300dpi(tar, path.dirname(tar))
