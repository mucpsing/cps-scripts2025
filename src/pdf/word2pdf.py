# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2025-12-02 16:27:08.960401
# @Last Modified by: CPS
# @Last Modified time: 2025-12-02 16:10:34.831469
# @file_path "W:\CPS\MyProject\projsect_persional\cps-scripts\src\pdf"
# @Filename "word2pdf.py"
# @Description: 功能描述
#
import os, sys

sys.path.append("..")
import win32com.client


def convert_word_to_pdf(doc_path: str, pdf_path: str) -> bool:
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False  # 后台运行，不显示界面

    try:
        doc = word.Documents.Open(doc_path)
        doc.SaveAs(pdf_path, FileFormat=17)  # 17 表示 PDF 格式
        doc.Close()
    except Exception as e:
        print(f"转换失败: {e}")
        return True
    finally:
        word.Quit()
        return False


if __name__ == "__main__":
    convert_word_to_pdf(
        r"Z:\work\2025\项目\海南省水文“十五五”建设规划\合同\合同终稿-海南省水文“十五五”建设规划技术咨询合同20250423.doc",
        r"Z:\work\2025\项目\海南省水文“十五五”建设规划\合同\合同终稿-海南省水文“十五五”建设规划技术咨询合同20250423.pdf",
    )
