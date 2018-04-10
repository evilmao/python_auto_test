# -*- coding:utf-8 -*-

# author by Failymao
'''
- 新增自动生成html测试报告
'''
import os
import time
import unittest
import ddt
from src.test.common.browser import Browser  # Screen
from src.test.page.xstz_injection_page import InjectionPage
from src.test.page.xstz_login_page import XSTZLoginPage
from src.test.page.xstz_payway_select import ChannelSelect
from src.utils.config import Config, DATA_PATH
from src.utils.support import get_func_name


Web_data = {"suite": {}}


def TestData():
    '''数据驱动数据函数'''
    try:
        from src.utils.ddt_testdata import testData
        from src.utils.file_reader import ExcelReader
        excelpath = DATA_PATH + "/xstz.xlsx"
        AssertData = ExcelReader(excelpath).data
        testData1 = []
        for i in AssertData:
            for testdata in testData:
                if testdata["P_name"] == i["P_name"]:
                    testdata["locator"] = i["locator"]
                    testdata["element"] = i["element"]
                    testData1.append(testdata)
        return testData1
    except TimeoutError:
        return None
        print("服务器超时！")


@ddt.ddt
class XSTZ_Web(unittest.TestCase):
    '''XSTZ_Web测试'''
    URL = Config().get('URL')
    USERNAME = Config().get('USERNAME')
    PWD = Config().get('PWD')
    browser = Browser(browser_type='firefox')
    driver = browser.open_browser(
        URL, maximize_window=False)

    @classmethod
    def setUpClass(cls):  # 初始化页面，传入浏览器类型，并打开浏览器
        print("Web starting test...")

    def bypass_auth(self):
        '''备用：绕过验证码--添加cookie'''
        driver = self.driver
        driver.add_cookie(
            {'name': u'logintoken',
             'value': u'eyJBY2NvdW50Ijo1MjAwMDMxMiwiRXhwIjoxNTE5NTI0ODUwOTEzL\
             CJMb2dpblR5cGUiOjAsIkFwcGx5IjoicGMiLCJOYW1lIjoi5rWL6K%2BV6a2P5bC\
             P5LicIn0%3D.ZWFrZjRMcTh0alRxdjB5US9qTTB0dm5mL2h5eVRZdnduWFpDa0s0\
             bkdVd1ZCUm5oRjJlcHZSRExrNkd4a2lGR0czY0JKWkVhWUM4OVd3eFEwMzI2eGpq\
             WXlnWFp4aGdSR1FEc0JpbWZNVm9yY0l0ajMwQ2w1UExEeW5NMzhuYVlTSWZHVWl0\
             Z2pKYUtxYm9OeHpUMjVWb2hSanB1NFBnZi9NRlZpOXpOUDFZPQ%3D%3D\jia'}
        )
        driver.add_cookie({'name': 'XSMCFX_UC_ACCOUNT',
                           'value': '=%2052000312%20'})
        return driver

    #@Screen(driver)
    def test_1_login(self):
        """ PC 登录测试"""
        test_action = get_func_name()                            # 获取当前测试行为，以测试函数命名规范获取
        LoginPage = XSTZLoginPage(self.driver)                   # 登录页面类
        LoginPage.login(self.USERNAME, self.PWD)                 # 登录，输入用户名，密码
        result = LoginPage.is_login_success                      # 验证点
        data1 = {}
        data1[test_action] = result["data"]
        Web_data["suite"].update(data1)
        self.assertTrue(result["result"])
        self.assertTrue(result["result"], msg=result["Exception"])

    #@Screen(driver)
    def test_2_injection(self):
        '''注资页面跳转'''
        test_action = get_func_name()
        JPage = InjectionPage(self.driver)                       # 网上存款页面类
        JPage.click_injection_button
        JPage.into_bank_page
        result = JPage.is_injection_success                       # 验证点
        data1 = {}
        data1[test_action] = result["data"]
        Web_data["suite"].update(data1)
        self.assertTrue(result["result"], msg=result["Exception"])

    @ddt.data(*TestData())  # 数据驱动模型
    #@Screen(driver)
    def test_3_payway(self, data):
        '''支付通道跳转'''
        money = Config().get("money")
        test_action = get_func_name()
        DPage = ChannelSelect(self.driver)                       # 支付通道页面类
        payway = DPage.select_payway(data["P_number"])
        if data["PB_number"]:                                    # 判断支付通道是否存在银行注资通道
            msg = DPage.select_bank(data["PB_number"])           # 获取当前测试银行名字
            print(msg)
        DPage.input_money(money)                                 # 提交
        result = DPage.is_deposit_success(
            data["locator"], data["element"])                    # 验证点
        time.sleep(1)
        data1 = {}
        print("当前测试通道：{}".format(payway))
        data1[test_action] = result["data"]

        Web_data["suite"].update(data1)
        self.assertTrue(result["result"], msg=result["Exception"])

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == '__main__':
    from src.utils.DingDingReport import ding_report
    from src.utils.Insert_InfluxDB import insert_influxdb
    from src.utils.HTMLTestRunner_Echarts import HTMLTestRunner
    from src.utils.config import REPORT_PATH

    now = time.strftime("%Y%m%d%H%M", time.localtime())
    report_name = "report_%s.html" % (now)
    report_path = os.path.join(REPORT_PATH, report_name)
    REPORT_URL = Config().get("report_url")
    report_url = REPORT_URL % report_name  # 重新定义report_url
    Test_date = time.strftime('%Y-%m-%d %H:%M:%S')

    Web_data["report_url"] = report_url
    Web_data["Test_date"] = Test_date

    title = "鑫圣投资"
    description = 'Web端测试'
    test_suite = unittest.TestSuite(unittest.makeSuite(XSTZ_Web))

    with open(report_path, 'wb') as f:
        runner = HTMLTestRunner(
            f, verbosity=2, title=title, description=description)
        runner.run(test_suite)

    insert_influxdb(Web_data)                                # 插入数据库
    ding_report(**Web_data)                                  # 钉钉机器人自动播报
    print(Web_data)
