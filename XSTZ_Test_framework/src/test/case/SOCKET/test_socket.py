# -*- coding:utf-8 -*-
# author by Failymao

'''
- socket接口测试用例 --client端
'''

import unittest
from src.utils.client import TCPClient
from src.utils.config import Config
from src.utils.extractor import JMESPathExtractor

je = JMESPathExtractor()


class TestAdd(unittest.TestCase):

    def setUp(self):
        c = Config()
        ip = c.get('ip')
        port = c.get('port')
        self.client = TCPClient(ip, port)

    def tearDown(self):
        self.client.close()

    def test_add(self):
        data = {
            'action': 'add',
            'params': {'a': 1, 'b': 2}
        }
        res = self.client.send(data, dtype='json')

        self.assertEqual(je.extract('result', res), 3)
        self.assertEqual(je.extract('action', res), 'add')

    def test_wrong_action(self):
        data = {
            'action': 'sub',
            'params': {'a': 1, 'b': 2}
        }
        res = self.client.send(data, dtype='json')

        self.assertEqual(je.extract('code', res), -2)
        self.assertEqual(je.extract('message', res), 'Wrong Action')

    def test_wrong_data(self):
        data = '111'
        res = self.client.send(data)
        self.assertEqual(je.extract('code', res), -1)
        self.assertEqual(je.extract('message', res), 'Data Error')


if __name__ == '__main__':
    unittest.main(verbosity=2)
