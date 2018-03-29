# -- coding:utf-8 --
# author by Failymao
'''
- payment way page class
- 继承XSTZLoginPage登录页面封装
'''
import time
from selenium.webdriver.common.by import By
from src.utils.log import logger
from .xstz_injection_page import InjectionPage


class ChannelSelect(InjectionPage):
    '''Operate the payment page'''
    loc_input_money = (By.ID, "money")                           # 金额输入框
    loc_next_step = (By.ID, "btnDeposit")                        # 下一步按键
    loc_paywayName = (By.ID, "paywayName")
    loc_submit_button = (By.ID, "btn_submit")                    # 提交按键
    loc_ensure_pay = (By.LINK_TEXT, "已完成付款")               # 跳转后
    loc_bank_inbox = (By.CSS_SELECTOR, '#bank_dom > div > i')    # 下拉框按键
    loc_bank_list = (By.CLASS_NAME, 'w-select-ul')               # 定位可选银行区域
    loc_bank_detail = (By.TAG_NAME, 'li')                        # 银行明细

    def select_payway(self, cn=0):
        '''pay way name method'''
        try:
            self.payways_elements[cn].click()                       # 选择支付通道一
            payway = self.payways_elements[cn].text                 # 获取支付通道名字
            return payway
        except Exception:
            logger.error("Payway does not exist")

    def sumbit(self, money):
        '''提交操作'''
        try:
            self.clear(self.loc_input_money)
            self.type(money, self.loc_input_money)
            self.click(self.loc_next_step)
            self.click(self.loc_submit_button)
            # self.switch_to_altet                                #
            # 接受弹窗，此处为提交时，浏览器安全提示
            time.sleep(2)
            logger.info("jumping to payment page 。。。")
        except Exception as e:
            logger.error("Error .Reason:{}".format(e))

    @property
    def exchange_bank_page(self):
        '''turn to bank payment page'''
        try:
            handles = self.collect_handles
            current_handle = self.current_window
            for handle in handles:
                if handle != current_handle:
                    self.exchange_to_window(handle)           # 切换到到第三方支付页面
                    logger.info(
                        'switch bank page!Page handle: {}'.format(handle))
                    return current_handle
        except Exception as e:
            logger.error("{}".format(e))

    def close_bank_page(self, bank_handle):
        '''close bank page,return to payment page'''
        try:
            self.close                              # 关闭第三方支付页面
            self.exchange_to_window(bank_handle)    # 返回支付页面
            logger.info("return to payment page!")
        except Exception as e:
            logger.error("Error ！Reason:{}".format(e))

    @property
    def return_payment_page(self):  # 点击确认，已完成付款！返回支付页面
        self.click(self.loc_ensure_pay)

    def select_bank(self, bn):
        self.click(self.loc_bank_inbox)
        banks = self.find_element(
            self.loc_bank_list).find_elements(self.loc_bank_detail)  # 二次定位
        banks[bn].click()
        return banks[bn].text

    def is_deposit_success(self, locator, element):

        bank_handle = self.exchange_bank_page
        try:
            self.find_element((locator, element))
            IsSuccess = "success"
            ReturnCode = 0
            result = True
            error_info = None
            print("Test Success!\n ")
            logger.info("第三方支付跳转成功")
        except Exception:
            error_info = self.save_screen_shot()  # 错误时保存截图:图片名称
            ReturnCode = 1
            IsSuccess = "Fail"
            result = False
            print("Test fail!")
            logger.error("支付页面崩溃或超时!")
        finally:
            self.close_bank_page(bank_handle)
            self.return_payment_page
            payload = {"result": result,
                       "data": {"ReturnCode": ReturnCode,
                                "IsSuccess": IsSuccess,
                                },
                       "Exception": error_info
                       }
            return payload
