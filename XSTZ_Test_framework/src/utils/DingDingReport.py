# -*- coding:utf-8 -*-
# author by Failymao

'''
- 钉钉机器人对测试结果进行指定@负责人实时播报
'''
import json
import requests
from src.utils.config import Config
from src.utils.log import logger


userlist = ["13636269356"]


def ding_report(**data):  # 钉钉机器人播报
    url = Config().get("dd_api")
    header = {
        "Content-Type": "application/json",
        "charset": "utf-8"
    }
    test_action = []
    suite_number = len(data["suite"])
    flag = 0

    if data:
        for k, v in data["suite"].items():
            test_action.append(k)
            if "Website" in v.keys():
                Website = v["Website"]
            elif v["ReturnCode"] == 0:
                flag += 1
        format_data = '&ensp;' * 10
        action = '</br>{}'.format(format_data).join(test_action)
        ding_data = {
            "msgtype": "markdown",
            "markdown": {"title": "XSTZ测试结果",
                         "text": "#### XSTZ自动化测试@13636269356\n " +
                         "> 用例个数：{}\n".format(suite_number) + '\n' +
                         "> 测试行为：{}\n " .format(action) + '\n' +
                         "> 测试站点：{}\n ".format(Website) + '\n' +
                         "> 测试结果：**Success:{}**\n ".format(flag) + '\n' +
                         "> **{0}Error:{1}**\n".format(format_data, suite_number - flag) + '\n' +
                         # "> 测试账号：{login_account} \n " .format(**data) + '\n'
                         "> ##### 测试时间：{Test_date}[[详情]({report_url})]"
                         .format(**data)
                         },
            "at": {
                "atMobiles": userlist,
                "isAtAll": False}
        }

    try:
        sendData = json.dumps(ding_data)
        requests.post(url, data=sendData, headers=header)
        logger.info("Dingding Robot call successfully！")
    except Exception as e:
        logger.info("send fail！{}".format(str(e)))


if __name__ == "__main__":
    pass
