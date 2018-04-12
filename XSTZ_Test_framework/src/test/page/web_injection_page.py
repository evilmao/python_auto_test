# -- coding:utf-8 --
# author by Failymao
"""
- 封装网上存款页面跳转类
- 验证登录成功后，定位验证登录信息
"""
import sys
from selenium.webdriver.common.by import By
from ...utils.log import logger
from .web_login_page import XSTZLoginPage


class InjectionPage(XSTZLoginPage):  # 继承STZLoginPage类
    loc_injection_link = (By.LINK_TEXT, u"网上存款")  # 定位存款操作按钮
    loc_Payways = (By.CSS_SELECTOR, '#paywayCheck >a')  # 获取当前支付通道个数
    loc_bank_inbox = (By.CSS_SELECTOR, '#bank_dom > div > i')  # 下拉框按键
    loc_bank_list = (By.CSS_SELECTOR, '#bank_dom > ul')  # 定位可选银行区域
    loc_bank_detail = (By.TAG_NAME, 'li')  # 银行明细

    @property
    def click_injection_button(self):  # 点击"网上存款"连接按键
        self.click(self.loc_injection_link)
        self.sleep(2)

    @property
    def into_bank_page(self):
        '''切换到支付通道页面'''
        try:
            handles = self.collect_handles
            current_handle = self.current_window
            for handle in handles:
                if handle != current_handle:
                    logger.info('switch to second window {}'.format(handle))
                    self.close  # 关闭当前页面
                    logger.info(
                        "close the page,handle {}".format(current_handle))
                    self.exchange_to_window(handle)
                    self.sleep(2)
        except Exception as e:
            logger.error(str(e))

    @property
    def payways_elements(self):  #
        '''获取当前支付通道元素个数'''
        payway_els = self.find_elements(self.loc_Payways)
        return payway_els

    @property
    def get_banks_elements(self):
        '''获取某个通道下的银行列表'''
        self.click(self.loc_bank_inbox)
        bank_elements = self.find_element(
            self.loc_bank_list).find_elements(self.loc_bank_detail)  # 二次定位
        return bank_elements

    @property
    def is_injection_success(self):
        try:
            n = self.elements_length(self.loc_Payways)  # 打开新的网页后获得支付通道数
            payway_names = ' | '.join(
                [name.text for name in self.payways_elements])
            IsSuccess = "success"
            ReturnCode = 0
            result = True
            error_info = None
            print("Test Success!\n ")
            print("当前可用支付通道数目：{}\n".format(n))
            print("通道明细：{}".format(payway_names))
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

    @property
    def get_payway_detail1(self):
        '''
        Returns:
            :payway_detail_info is a dict type.It was used to store the detail info of
            bank and payway info.
            for example:

            [ {"P_number":1,"P_name:"通道一","P_bank":None},
              {"P_number":2,"P_name:"通道二","P_bank":None}，
              {"P_number":3,"P_name:"通道三",
                                             "P_bank":[{"B_number":0,"B_name":"工商银行"}，
                                                       {"B_number":1,"B_name":"建设银行"}，
                                                        ...
                                                        ]
             ]
            :payway_info = {"P_number":n,"P_name":payway_name,"P_bank":None}
            :P_bank = if bank_dic:[bank_dic]
            :P_number from "n"
            :P_name from "payway_name"
            :P_banks if "bank_elements":bank_dic,else: None
            :B_name from "bank.text"
            :B_number from "k"
        '''
        payway_detail_info = []
        payway_list = []
        for n, element in enumerate(self.payways_elements):
            bank_detail = {}
            payway_info = {"P_number": None,
                           "P_name": None,
                           "P_banks": None}

            element.click()              # 选择通道
            payway_name = element.text   # 获取支付通道名字
            try:
                bank_elements = self.get_banks_elements
                bank_list = [bank.text for bank in bank_elements]
                bank_dic = {k: v for k, v in enumerate(bank_list)}
                bank_detail[payway_name] = bank_dic
                payway_info["P_banks"] = bank_dic
            except Exception:
                payway_info["P_banks"] = None

            payway_info["P_number"] = n
            payway_info["P_name"] = payway_name
            payway_list.append(payway_name)
            payway_detail_info.append(payway_info)

        payway_str = ' | '.join(payway_list)
        return payway_detail_info, payway_str


if __name__ == "__main__":
    print(sys.path)
