# -- coding:utf-8 --
# author by Failymao
"""
- 封装xstz登录首页：进行页面操作--登录操作
- 3.18优化代码
"""

import re
from selenium.webdriver.common.by import By
from src.test.common.page import BasePage
from src.utils.log import logger


class XSTZLoginPage(BasePage):  # 继承自Page类
    loc_account_input = (By.XPATH, "//div[2]/div[2]/div/input")
    loc_passwd_input = (By.XPATH, "//div[2]/input")
    loc_login_button = (By.ID, 'loginStatus')
    loc_login_result = (By.XPATH, "//[@id='divCard']/p[1]")  # 定位登录成功欢迎信息
    loc_login_account = (By.CSS_SELECTOR, ".ac-account2")  # 定位账户信息位置
    loc_logout_button = (By.XPATH, "//a[@id='btnLogout']/span")  # 定位退出按钮
    loc_logout_alert = (By.LINK_TEXT, u"确 定")

    def login(self, USERNAME, PWD):
        '''input account&password'''
        self.type(USERNAME, self.loc_account_input)
        self.type(PWD, self.loc_passwd_input)
        self.click(self.loc_login_button)

    def title(self):
        '''get title and parse_title'''
        page_title = self.get_page_title
        pattern = re.compile(u'\((.*)\)')  # 修正title正则匹配
        match = pattern.search(page_title)
        if match:
            return match.group(1)

    @property
    def login_accout(self):
        result_account = self.get_el_text(self.loc_login_account)
        return result_account

    @property
    def logout(self):
        self.click(self.loc_logout_button)
        self.click(self.loc_logout_alert)

    @property
    def is_login_success(self):
        '''
        Assert function: judge is it success! Collect useful data 
        '''
        Website = self.title()             # 解析服务器地址
        try:
            self.sleep(1)
            account = self.login_accout
            IsSuccess = "success"
            ReturnCode = 0
            result = True
            format_logger = ' ' * 43
            error_info = None
            logger.info(
                "{4}！\n{0}- 测试账户：{1}\n{2}- 服务器地址:{3}".format(format_logger, account, format_logger, Website, IsSuccess))
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
                                "IsSuccess": IsSuccess,
                                "Website": Website
                                },
                       "Exception": error_info

                       }
            return payload
