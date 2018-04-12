# -*- coding:utf-8 -*-
# author by Failymao

'''
- 支付通道详情页面类
- 验证点:选择某一银行后,获取页面上订单号,判定测试通过
'''
from appium.webdriver.common.mobileby import MobileBy
from faker.providers import bank

from ...utils.log import logger
from .web_injection_page import InjectionPage


class ChannelSelect(InjectionPage):
    loc_input_money = (
        MobileBy.XPATH, '//android.widget.FrameLayout/\
        android.webkit.WebView/android.view.View/android.view.View[4]/android.widget.EditText')  # 金额选择框
    loc_ensure_button = (MobileBy.ACCESSIBILITY_ID, '确定 Link')  # 默认选择
    loc_pay_button = (MobileBy.ACCESSIBILITY_ID, '支付 Link')
    loc_agree_checkbox = (MobileBy.ACCESSIBILITY_ID, '本人已阅读以下注意事项')

    loc_bank_select = (MobileBy.XPATH, '//android.widget.FrameLayout/\
    android.webkit.WebView/android.view.View/android.widget.ListView[1]/android.view.View')
    a1 = (MobileBy.XPATH, '//android.widget.FrameLayout/\
    android.webkit.WebView/android.view.View/android.widget.ListView[1]/android.view.View[{}]/android.view.View[1]')

    b1 = (MobileBy.XPATH,
          '//android.widget.FrameLayout/android.webkit.WebView/android.view.View/android.view.View/android.view.View[6]/android.view.View[2]')

    @property
    def select_money(self):
        '''金额输入框选择金额,并点击确认'''
        try:
            self.click(self.loc_input_money)
            self.sleep(1)
            self.click(self.loc_ensure_button)
        except Exception as e:
            print(e)

    @property
    def select_payway(self):
        '''点击支付按钮'''
        # self.click(self.loc_agree_checkbox)  # 同意contract
        self.click(self.loc_pay_button)     # click pay button

    @property
    def select_bank(self):
        '''获取当前银行卡信息'''
        import re
        import random
        try:
            Bank_eles = self.find_elements(self.loc_bank_select)  # 定位到银行展示区域
    #         for i in range(1, len(Bank_eles) - 2, 2):             # 根据获取的元素多少,获得对应当前 银行卡数
    #             a2 = (self.a1[0], self.a1[1].format(i + 1))
            i = random.randrange(1, len(Bank_eles) - 2, 2)
            Bank_eles[i].click()

            order_number = self.find_element(self.b1).get_attribute('name')
    #             bankname = self.find_element(a2).get_attribute('name')
    #             pa = re.compile('(.*?)\(')
    #             match = pa.search(bankname)
    #             if match:
    #                 bank_name = match.group(1)
    #                 bank_list.append(bank_name)
    #         bank_str = '\n'.join(list(set(bank_list)))
    #         print('当前银行信息:{}'.format(bank_str))
            print(order_number)
        except Exception as e:
            print(e)

    def into_bank_page(self):
        pass
