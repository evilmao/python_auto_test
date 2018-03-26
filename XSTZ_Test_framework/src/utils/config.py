# -*- coding:utf-8 -*-
# author by Failymao
"""
读取配置yaml，也可用其他如XML,INI等，
需在file_reader中添加相应的Reader进行处理。
"""
import os
from .file_reader import YamlReader

# 通过当前文件的绝对路径，其父级目录一定是框架的base目录，然后确定各层的绝对路径。如果你的结构不同，可自行修改。
# 之前直接拼接的路径，修改了一下，用现在下面这种方法，可以支持linux和windows等不同的平台，也建议大家多用os.path.split()和os.path.join()，不要直接+'\\xxx\\ss'这样
BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
BASE_DIR = os.path.split(BASE_PATH)[0]
CONFIG_FILE = os.path.join(BASE_DIR, 'config', 'config.yaml')
DATA_PATH = os.path.join(BASE_DIR, 'data')
DRIVER_PATH = os.path.join(BASE_DIR, 'drivers')
LOG_PATH = os.path.join(BASE_DIR, 'log')
REPORT_PATH = os.path.join(BASE_DIR, 'report')


class Config:
    def __init__(self, config=CONFIG_FILE):
        self.config = YamlReader(config).data

    def get(self, element, index=0):
        return self.config[index].get(element)


if __name__ == "__main__":
    a = Config()
    print(a.config)
