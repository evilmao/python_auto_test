# -*- coding:utf-8 -*-
# author by Failymao

'''组织测试案例,运行测试程序'''
import unittest
from src.test.case.UI.XSTZ_WAP import Config, XSTZ_TEST, report_path
from src.utils.HTMLTestRunner_Echarts import HTMLTestRunner
from src.utils.SendEmail import Email


def send_email(data):  # 发送emil
    g = Config().get('email')
    e = Email(title=g.get('title'),
              message=g.get('message'),
              receiver=g.get('receiver'),
              HOST=g.get('HOST'),
              sender=g.get('sender'),
              password=g.get('password'),
              path=data
              )
    e.send()


def main():
    title = "鑫圣投资"
    description = 'Web端测试'
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(
        XSTZ_TEST, "test_login"))
    test_suite.addTest(unittest.makeSuite(
        XSTZ_TEST, "test_injection_page"))
    test_suite.addTest(unittest.makeSuite(XSTZ_TEST, "test_payway"))

    with open(report_path, 'wb') as f:
        runner = HTMLTestRunner(
            f, verbosity=2, title=title, description=description)
        runner.run(test_suite)
    send_email(report_path)


if __name__ == "__main__":
    main()
