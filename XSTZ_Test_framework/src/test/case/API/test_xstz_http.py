# -*- coding:utf-8 -*-
# author by Failymao
"""
- API接口测试--以百度为例
"""

import unittest
from src.utils.HTMLTestRunner_Echarts import HTMLTestRunner
from src.utils.assertion import assertHTTPCode
from src.utils.client import HTTPClient
from src.utils.config import Config, REPORT_PATH
from src.utils.log import logger


class TestBaiDuHTTP(unittest.TestCase):
    URL = Config().get('URL_BD')

    def setUp(self):
        self.client = HTTPClient(url=self.URL, method='GET')

    def test_baidu_http(self):
        res = self.client.send()
        logger.debug(res.text)
        assertHTTPCode(res, [400])
        self.assertIn('百度一下，你就知道', res.text)


if __name__ == '__main__':
    report = REPORT_PATH + '\\report_http.html'
    with open(report, 'wb') as f:
        runner = HTMLTestRunner(
            f, verbosity=2, title='从0搭建测试框架 灰蓝', description='接口html报告')
        runner.run(TestBaiDuHTTP('test_baidu_http'))
