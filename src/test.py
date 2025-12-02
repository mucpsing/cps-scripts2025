# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2025-12-02 17:04:22.595720
# @Last Modified by: CPS
# @Last Modified time: 2025-12-02 17:04:22.595720
# @file_path "W:\CPS\MyProject\projsect_persional\cps-scripts\src"
# @Filename "test.py"
# @Description: 功能描述
#
import os, sys

sys.path.append("..")

from os import path
from pathlib import Path
from pydantic import BaseModel

if __name__ == "__main__":
    print(Path(r"Z:\work\2025\项目\海南省水文“十五五”建设规划\合同\合同终稿-海南省水文“十五五”建设规划技术咨询合同20250423.doc").suffix.lower())
