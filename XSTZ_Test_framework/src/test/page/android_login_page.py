# -*- coding:utf-8 -*-
# author by Failymao
'''
- 安卓端'登录页面'封装
- 测试点: 如果页面获取账号,判断测试通过
'''

from selenium.webdriver.common.by import By
from src.test.common.page import BasePage
from src.utils.log import logger


class LoginPage(BasePage):
    local_close_ad = (By.ID, "com.xsjinye.xsforex:id/iv_mnds_close")
    local_portal = (By.ID, "com.xsjinye.xsforex:id/tab_mine")
    local_login_button = (By.ID, "com.xsjinye.xsforex:id/tv_login")
    loc_account_input = (By.ID, "com.xsjinye.xsforex:id/et_username")
    loc_passwd_input = (By.ID, "com.xsjinye.xsforex:id/et_password")

    @property
    def enter_portal(self):
        try:
            self.click(self.local_close_ad)
        except Exception:
            pass
        self.click(self.local_portal)

    def login(self, USERNAME, PWD):
        '''input account&password'''
        self.click(self.local_login_button)
        self.type(USERNAME, self.loc_account_input)
        self.type(PWD, self.loc_passwd_input)
        self.click(self.local_login_button)

    @property
    def login_account(self):
        self.click(self.local_close_ad)
        self.click(self.local_portal)
        result = self.get_el_text(self.local_login_button)
        return result

    @property
    def is_login_success(self):
        '''
        Assert function: judge is it success! Collect useful data 
        '''

        try:
            self.sleep(1)
            account = self.login_account
            IsSuccess = "success"
            ReturnCode = 0
            result = True
            format_logger = ' ' * 43
            error_info = None
            logger.info(
                "{3}！\n{0}- 测试账户：{1}\n{2}".format(format_logger, account, format_logger, IsSuccess))
            print("Test success!")
            print("Test Account:{}".format(account))
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
                                "IsSuccess": IsSuccess
                                },
                       "Exception": error_info

                       }
            return payload
