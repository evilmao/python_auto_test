# -*- coding:utf-8 -*-
# author by Failymao
'''
- 支付通道1页面类封装
- 继承XSTZLoginPage登录页面封装
'''

import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from src.utils.log import logger
from .xstz_injection_page import InjectionPage


class Channel1Page(InjectionPage):
    '''Channel 1 page'''
    loc_input_money = (By.ID, "money")  # 金额输入框
    loc_next_step = (By.ID, "btnDeposit")  # 下一步按键
    loc_paywayName = (By.ID, "paywayName")  # 确认支付页，获取支付通道名
    loc_submit_button = (By.ID, "btn_submit")  # 提交按键
    loc_ensure_pay = (By.LINK_TEXT, "已完成付款")  # 跳转后
    loc_cardNo_inbox = (By.XPATH, "//*[@id='cardNumber']")

    def get_payway_name(self, cn=0):
        self.payways_elements[cn].click()  # 选择支付通道一
        payway = self.payways_elements[cn].text  # 获取支付通道名字
        return payway

    def sumbit(self, money):
        '''提交操作'''
        try:
            self.clear(*self.loc_input_money)  # 清除金额输入框
            self.type(money, *self.loc_input_money)  # 重新输入金额
            self.click(*self.loc_next_step)  # 点击下一步
            self.click(*self.loc_submit_button)  # 提交
            self.switch_to_altet  # 接受弹窗，此处为提交时，浏览器安全提示
            time.sleep(1)
            logger.info("正在跳转网银支付页面。。。")
        except Exception as e:
            logger.error("跳转失败！Reason:{}".format(e))

    @property
    def is_loc_CardNoElement(self):  # 判断页面是否加载到输入框元素是否可见
        driver = self.driver
        try:
            element = WebDriverWait(driver, 10, poll_frequency=0.3).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='cardNumber']")))
            print(element)
            return element
        except Exception as e:
            logger.error("页面加载失败!{}".format(e))

    @property
    def return_code(self):
        import requests
        '''获取网银支付页面状态码'''
        try:
            handles = self.collect_handles
            current_handle = self.current_window

            for handle in handles:
                if handle != current_handle:
                    logger.info('switch to second window {}'.format(handle))
                    self.exchange_to_window(handle)  # 切换到到第三方支付页面
                    time.sleep(2)
                    #element = self.is_loc_CardNoElement
                    url = self.get_current_url
                    logger.info('The url:{}'.format(url))
                    code = requests.get(url).status_code
                    logger.info('Response status code:{}'.format(code))
                    self.exchange_to_window(current_handle)  # 返回支付页面
                    return code  # 使用requests库获取返回的状态码
        except Exception as e:
            logger.error("{}".format(e))

    @property
    def get_status_code(self):  # 打开网银页面，获取状态码，关闭页面，返回支付页面
        code = self.return_code
        self.click(*self.loc_ensure_pay)
        return code


class Channel2Page(Channel1Page):
    '''Channel 2 page'''
    loc_bank_inbox = (By.CSS_SELECTOR, '#bank_dom > div > i')  # 下拉框按键
    loc_bank_list = (By.CLASS_NAME, 'w-select-ul')  # 定位可选银行区域
    loc_bank_detail = (By.TAG_NAME, 'li')   # 银行明细

    @property
    def get_bank_detail(self):
        '''获取银行明细，随机抽查某个银行进行测试'''
        self.click(*self.loc_bank_inbox)
        # 获得支付通道支持银行elements
        banks = self.find_element(
            *self.loc_bank_list).find_elements(*self.loc_bank_detail)  # 二次定位
        bn = len(banks)
        n = random.randint(0, bn)
        test_bank = banks[n].text
        bank_list = [bank.text for bank in banks]
        banks[n].click()
        return test_bank, bank_list
