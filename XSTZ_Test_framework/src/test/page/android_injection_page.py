# -*- coding:utf-8 -*-
# author by Failymao

'''
- Android端 注资跳转 page封装
- ♥ 注意xpath定位方式
- 验证点:获取测试人员信息,及测试通道信息,判断测试通过

'''


from selenium.webdriver.common.by import By
from ...utils.log import logger
from .web_login_page import XSTZLoginPage


class InjectionPage(XSTZLoginPage):
    loc_injection_button = (
        By.ID, "com.xsjinye.xsforex:id/ll_put_money")  # 网上存款跳转
    loc_account = (
        By.XPATH, '//android.widget.FrameLayout/\
        android.webkit.WebView/android.view.View/android.view.View[2]')
    locl_payway_name = (
        By.XPATH, '//android.widget.FrameLayout/\
        android.webkit.WebView/android.view.View/android.view.View[8]')
    local_payway_remark = (
        By.XPATH, '//android.widget.FrameLayout/\
        android.webkit.WebView/android.view.View/android.view.View[9]')

    @property
    def click_injection_button(self):  # 点击"网上存款"连接按键
        self.click(self.loc_injection_button)
        self.sleep(2)

    @property
    def get_payway_detail(self):
        try:
            payway_name = self.find_element(
                self.locl_payway_name).get_attribute('name')
            payway_remark = self.find_element(
                self.local_payway_remark).get_attribute('name')
            payway_info = '{0}:{1}'.format(payway_name, payway_remark)
            return payway_info
        except Exception as e:
            print(e)

    @property
    def is_injection_success(self):
        try:
            Account_name = self.find_element(
                self.loc_account).get_attribute('name')
            payway_info = self.get_payway_detail
            IsSuccess = "success"
            ReturnCode = 0
            result = True
            error_info = None
            print("Test Success!\n ")
            print("Test Name:{}".format(Account_name))
            print("Payway Info:{}".format(payway_info))
        except Exception as e:
            error_info = self.save_screen_shot()  # 错误时保存截图:图片名称
            logger.error("Test Fail！Reason:{}".format(str(e)))
            ReturnCode = 1
            IsSuccess = "Fail"
            result = False,
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
