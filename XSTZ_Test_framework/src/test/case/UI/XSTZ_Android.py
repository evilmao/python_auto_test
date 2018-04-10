# -*- coding:utf-8 -*-
# author by Failymao

'''
- Android 端测试用例
'''
import os
import time
import unittest
from appium import webdriver
from src.test.page.app_login_page import LoginPage
from src.utils.config import Config
from src.utils.support import get_func_name


Android_data = {"suite": {}}


class XSTZ_Android(unittest.TestCase):
    '''Android端测试'''
    USERNAME = Config().get("USERNAME")
    PWD = Config().get("PWD")
    desired_caps = Config().get("desired_caps")
    Remote_URL = Config().get("Remote_URL")
    driver = webdriver.Remote(Remote_URL, desired_caps)  # 打开测试XSTZ程序主页
    driver.implicitly_wait(30)

    @classmethod
    def setUpClass(cls):
        print("Android starting test...")

    def test_Android_1_login(self):
        '''Android 登录测试'''
        test_action = get_func_name()
        Login = LoginPage(self.driver)
        Login.enter_portal
        Login.login(self.USERNAME, self.PWD)
        result = Login.is_login_success
        data1 = {}
        data1[test_action] = result["data"]
        Android_data["suite"].update(data1)
        self.assertTrue(result["result"], msg=result["Exception"])

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    from src.utils.HTMLTestRunner_Echarts import HTMLTestRunner
    from src.utils.config import REPORT_PATH
    from src.utils.DingDingReport import ding_report
    from src.utils.Insert_InfluxDB import insert_influxdb

    REPORT_URL = Config().get("report_url")
    now = time.strftime("%Y%m%d%H%M", time.localtime())
    report_name = "report_%s.html" % (now)
    report_path = os.path.join(REPORT_PATH, report_name)
    report_url = REPORT_URL % report_name  # 重新定义report_url
    Test_date = time.strftime('%Y-%m-%d %H:%M:%S')

    Android_data["report_url"] = report_url
    Android_data["Test_date"] = Test_date

    title = "鑫圣投资"
    description = 'Android端测试'
    test_suite = unittest.TestSuite(unittest.makeSuite(XSTZ_Android))

    with open(report_path, 'wb') as f:
        runner = HTMLTestRunner(
            f, verbosity=2, title=title, description=description)
        runner.run(test_suite)

    insert_influxdb(Android_data)                                # 插入数据库
    ding_report(**Android_data)                                  # 钉钉机器人自动播报
    print(Android_data)
