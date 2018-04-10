# -*- coding:utf-8 -*-
# author by Failymao

'''组织测试案例,运行测试程序'''

import os
import time
import unittest
from src.test.case.UI.XSTZ_Android import XSTZ_Android, Android_data
from src.test.case.UI.XSTZ_WEB import XSTZ_Web, Web_data
from src.utils.DingDingReport import ding_report
from src.utils.HTMLTestRunner_Echarts import HTMLTestRunner
from src.utils.Insert_InfluxDB import insert_influxdb
from src.utils.SendEmail import Email
from src.utils.config import Config, REPORT_PATH


REPORT_URL = Config().get("report_url")
now = time.strftime("%Y%m%d%H%M", time.localtime())
report_name = "report_%s.html" % (now)
report_path = os.path.join(REPORT_PATH, report_name)
report_url = REPORT_URL % report_name  # 重新定义report_url


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


def run_all_suite():
    title = "鑫圣投资"
    description = 'Web&Android端测试'
    suite = unittest.TestSuite()

    suite = suite(unittest.makeSuite(XSTZ_Web))
    suite.addTest(unittest.makeSuite(XSTZ_Android))

    with open(report_path, 'wb') as f:
        runner = HTMLTestRunner(
            f, verbosity=2, title=title, description=description)
        runner.run(suite)


def main():
    run_all_suite()
    Test_date = time.strftime('%Y-%m-%d %H:%M:%S')
    Report_data = {"suite": {}}
    suite_data = Android_data["suite"]
    s = Web_data["suite"]
    suite_data.update(s)
    Report_data["report_url"] = report_url
    Report_data["Test_date"] = Test_date
    Report_data["suite"] = suite_data
    insert_influxdb(Report_data)                                # 插入数据库
    ding_report(**Report_data)                                  # 钉钉机器人自动播报
    send_email(report_path)


if __name__ == "__main__":
    main()
