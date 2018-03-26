# -*- coding:utf-8 -*-
# author by Failymao

'''
- 封装YamlReader类,用来读取yaml文件
- 添加ExcelReader类，实现读取excel内容,数据分离，进行参数化
'''
import os
from xlrd import open_workbook
import yaml


class YamlReader:
    """
         读取yaml文件中的内容。返回list。
    """

    def __init__(self, yamlf):
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError('文件不存在！')
        self._data = None  # 定义私有字段，只能内部调用

    @property
    def data(self):
        # 如果是第一次调用data，读取yaml文档，否则直接返回之前保存的数据
        if not self._data:
            with open(self.yamlf, 'rb') as f:
                # load后是个generator，用list组织成列表
                self._data = list(yaml.safe_load_all(f))

        return self._data  # 获取yaml的值以字典为元素的列表


class SheetTypeError(Exception):
    pass


class ExcelReader:
    '''读取excel文件中的内容。返回list'''

    def __init__(self, excelPath, sheet=0, title_line=True):
        if os.path.exists(excelPath):
            self.excel = excelPath  # 定义excel路径
        else:
            raise FileNotFoundError('文件不存在！')
        self.sheet = sheet  # 定义excel对应表名
        self.title_line = title_line  # 定义第一行为title
        self._data = list()  # 定义一个私有字段，用来读取数据，只能内部访问！

    @property
    def data(self):
        if not self._data:  # 如果文件不存在
            workbook = open_workbook(
                self.excel)  # 打开指定excel文件
            if type(self.sheet) not in [int, str]:
                raise SheetTypeError(
                    'Please pass in <type int> or <type str>, not {0}'.format(type(self.sheet)))
            elif type(self.sheet) == int:
                s = workbook.sheet_by_index(self.sheet)
            else:
                s = workbook.sheet_by_name(self.sheet)

            if self.title_line:
                title = s.row_values(0)  # 首行为title，0为首行
                for column in range(1, s.nrows):
                    # 依次遍历其余行，与首行组成dict，拼到self._data中
                    self._data.append(dict(zip(title, s.row_values(column))))
            else:
                for column in range(0, s.nrows):
                    # 遍历所有行，拼到self._data中
                    self._data.append(s.row_values(column))
        return self._data


if __name__ == '__main__':
    y = 'E:\GIT库版本库管理\automation\XSTZ_Test_framework\config\config.yaml'
    reader = YamlReader(y)
    print(reader.data)

    path = 'E:/GIT库版本库管理/automation/XSTZ_Test_framework/data/xstz.xlsx'
    reader = ExcelReader(path, sheet=0, title_line=True)
    print(reader.data)
