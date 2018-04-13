# -*- coding:utf-8 -*-
# author by Failymao

'''
- 支付通道详情页面类
- 验证点:选择某一银行后,获取页面上订单号,判定测试通过
'''
from appium.webdriver.common.mobileby import MobileBy
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
          '//android.webkit.WebView/android.view.View/android.view.View[6]/android.view.View[2]')

    @property
    def select_money(self):
        '''金额输入框选择金额,并点击确认'''
        try:
            self.click(self.loc_input_money)
            self.click(self.loc_ensure_button)
            logger.info("金额选择输入正常!")
        except Exception:
            raise Exception

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
            i = random.randrange(1, len(Bank_eles) - 2, 2)
            a2 = (self.a1[0], self.a1[1].format(i + 1))
            bankname = self.find_element(a2).get_attribute('name')
            pa = re.compile('(.*?)\(')
            match = pa.search(bankname)
            if match:
                bank_name = match.group(1)
            Bank_eles[i].click()
            order_number = self.find_element(self.b1).get_attribute('name')
            return bank_name, order_number
        except Exception:
            raise Exception

    @property
    def is_deposit_success(self):
        try:
            bank_name, order_number = self.select_bank
            IsSuccess = "success"
            ReturnCode = 0
            result = True
            error_info = None
            print("Test Success!\n ")
            print("Test Bank:{}".format(bank_name))
            print("Oder Info:{}".format(order_number))
        except Exception as e:
            error_info = self.save_screen_shot()  # 错误时保存截图:图片名称
            logger.error("Test Fail！Reason:{}".format(str(e)))
            ReturnCode = 1
            IsSuccess = "Fail"
            result = False
            print("Test fail!")
            print("Error Reason:{}".format(e))
        finally:
            payload = {"result": result,
                       "data": {"ReturnCode": ReturnCode,
                                "IsSuccess": IsSuccess,
                                },
                       "Exception": error_info
                       }
            return payload
