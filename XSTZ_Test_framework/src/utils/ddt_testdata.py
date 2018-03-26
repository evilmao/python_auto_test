# -*- coding:utf-8 -*-
# author by Failymao

from selenium import webdriver
from selenium.common.exceptions import TimeoutException  # 导入等待超时模块
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.utils.config import Config


SERVICE_ARGS = ['--load-images=false',
                '--disk-cache=true',
                '--ssl-protocol=any',
                '--ignore-ssl-errors=true'
                ]


class PayWayData:
    def __init__(self):
        self.driver = webdriver.PhantomJS(service_args=SERVICE_ARGS)
        self.wait = WebDriverWait(self.driver, 3, poll_frequency=0.1)
        url = Config().get("deposit_URL")
        self.driver.get(url)

    @property
    def payways_elements(self):
        loc_Payways = (By.CSS_SELECTOR, '#paywayCheck >a')  # 获取当前支付通道个数
        try:
            payway_els = self.wait.until(
                EC.presence_of_all_elements_located((loc_Payways)))
            return payway_els
        except TimeoutException:
            print("Timeout")

    @property
    def get_banks_elements(self):
        '''获取某个通道下的银行列表'''
        loc_bank_inbox = (By.CSS_SELECTOR, '.w-select-down')  # 下拉框按键
        bl = (By.CSS_SELECTOR, '.w-select-ul')                # 定位可选银行区域
        bd = (By.TAG_NAME, 'li')                              # 银行明细
        try:
            button = self.wait.until(
                EC.presence_of_element_located((loc_bank_inbox)))
            button.click()
            bank_elements = self.driver.find_element(
                bl[0], bl[1]).find_elements(bd[0], bd[1])      # 二次定位
            return bank_elements
        except Exception:
            pass

    @property
    def ddt_testData(self):
        '''Fetches payways and bank detail from deposit page.

        According  deposit page element get the number of payways and if banks elements
        exist, fetch the bank elements. Build the testDate which was used the source ddt 
        module data! 

        Returns:
            :payway_detail_info is a dict type.It was used to store the detail info of
            bank and payway info.
            for example:

            [ {"P_number":1,"P_name:"通道一","P_bank":None},
              {"P_number":2,"P_name:"通道二","P_bank":None}，
              {"P_number":3,"P_name:"通道三","PB_number":0},
              {"P_number":3,"P_name:"通道三","PB_number":1},
              {"P_number":3,"P_name:"通道三","PB_number":2},
                ....
             ]
            :testData = {"P_number":n,"P_name":payway_name,"P_bank":None}
            :P_number from "n"
            :P_name from "payway_name"
            :PB_number from PB_number
        '''
        import time
        testData = []
        try:
            for n, element in enumerate(self.payways_elements):
                payway_info = {}
                element.click()                                      # 选择通道
                time.sleep(0.1)
                payway_name = element.text                           # 获取支付通道名字
                try:
                    bs = self.get_banks_elements          # 获取支付通道下的银行通道个数
                    time.sleep(0.1)
                    for PB_number in range(len(bs)):
                        payway_info = {}
                        payway_info["P_number"] = n
                        payway_info["P_name"] = payway_name
                        payway_info["PB_number"] = PB_number
                        testData.append(payway_info)
                except Exception:
                    payway_info["P_number"] = n
                    payway_info["P_name"] = payway_name
                    payway_info["PB_number"] = None
                    testData.append(payway_info)
            return testData
        except TimeoutException:
            print("服务器连接超时")


testData = PayWayData().ddt_testData


if __name__ == "__main__":
    t = PayWayData()
    testData = t.ddt_testData
    print(testData)
