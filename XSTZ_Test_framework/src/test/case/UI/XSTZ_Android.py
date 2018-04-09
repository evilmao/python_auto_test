# -*- coding:utf-8 -*-
# author by Failymao

'''
- Android 端测试用例
'''
import os
import time
import unittest
from appium import webdriver
from src.test.common.subfunc import get_func_name
from src.test.page.app_login_page import LoginPage
from src.utils.HTMLTestRunner_Echarts import HTMLTestRunner
from src.utils.config import Config, REPORT_PATH


REPORT_URL = Config().get("report_url")
now = time.strftime("%Y%m%d%H%M", time.localtime())
report_name = "report_%s.html" % (now)
report_path = os.path.join(REPORT_PATH, report_name)
report_url = REPORT_URL % report_name  # 重新定义report_url

Test_date = time.strftime('%Y-%m-%d %H:%M:%S')
data = {"suite": {},
        "Test_date": Test_date,
        "report_url": report_url
        }


class XSTZ_Android(unittest.TestCase):
    USERNAME = Config().get("USERNAME")
    PWD = Config().get("PWD")
    desired_caps = Config().get("desired_caps")
    Remote_URL = Config().get("Remote_URL")
    driver = webdriver.Remote(Remote_URL, desired_caps)  # 打开测试XSTZ程序主页
    driver.implicitly_wait(30)

    @classmethod
    def setUpClass(cls):
        print("starting test on Android...")

    def test_Android_login(self):
        '''Android 登录测试'''
        test_action = get_func_name()
        Login = LoginPage(self.driver)
        Login.enter_portal
        Login.login(self.USERNAME, self.PWD)
        result = Login.is_login_success
        data1 = {}
        data1[test_action] = result["data"]
        data["suite"].update(data1)
        self.assertTrue(result["result"], msg=result["Exception"])

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    title = "鑫圣投资"
    description = 'Andriud端测试'
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(XSTZ_Android, "test_login"))

    with open(report_path, 'wb') as f:
        runner = HTMLTestRunner(
            f, verbosity=2, title=title, description=description)
        runner.run(test_suite)
    print(data)
