# -*- coding:utf-8 -*-
# author by Failymao

'''
-封装一个断言:当unittest无法满足断言时，需要封装自己的断言
'''


def assertHTTPCode(response, code_list=None):
    res_code = response.status_code
    if not code_list:
        code_list = [200]
    if res_code not in code_list:
        # 抛出AssertionError，unittest会自动判别为用例Failure，不是Error
        raise AssertionError('响应code不在列表中！')  # 自定义异常
