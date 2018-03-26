# -*- coding:utf-8 -*-
# author by Failymao
"""
- 封装页面操作的类--继承自Browser
"""
import os
import time
from selenium.common.exceptions import *   # 导入所有的异常类
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.utils.config import REPORT_PATH
from src.utils.log import logger


class BasePage(object):
    """ Base on Selenium frame"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout=5, poll_frequency=0.3)

    def quit_browser(self):
        '''close and quit browser'''
        self.driver.quit()

    def forward(self):
        '''forward operate'''
        self.driver.forward()
        logger.info("Click forward on current page.")

    def back(self):
        self.driver.back()
        logger.info("Click back on current page.")

    def wait(self, seconds):
        '''隐式等待'''
        self.driver.implicitly_wait(seconds)
        logger.info("wait for %d seconds." % seconds)

    @property
    def close(self):
        try:
            self.driver.close()
            logger.info("Closing the browser.")
        except NameError as e:
            logger.error("Failed to quit the browser with %s" % e)

    def save_screen_shot(self, name='XSTZ_WAP'):
        day = time.strftime('%Y%m%d', time.localtime(time.time()))
        screenshot_path = REPORT_PATH + '\screenshot_%s' % day

        if not os.path.exists(screenshot_path):
            os.makedirs(screenshot_path)
        rt = time.strftime('%H%M%S', time.localtime(time.time()))
        try:
            screenshot = self.driver.save_screenshot(
                screenshot_path + '\\%s_%s.png' % (name, rt))  # 截图命名及保存位置
            return screenshot
        except NameError as e:
            logger.error("Failed to take screenshot! %s" % e)
            self.get_windows_img()

    def find_element(self, locator):
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            logger.info("Had find the element {}".format(element.text))
            return element
        except NoSuchElementException as e:
            logger.error("NoSuchElementException: %s" % e)

    def find_elements(self, locator):
        try:
            elements = self.wait.until(
                EC.presence_of_all_elements_located(locator))
            logger.info("Had find the element {}".format(len(elements)))
            return elements
        except NoSuchElementException as e:
            logger.error("NoSuchElementException: %s" % e)

    def type(self, text, locator):
        el = self.find_element(locator)
        el.clear()
        try:
            el.send_keys(text)
            logger.info("Had type \' %s \' in inputBox" % text)
        except NameError as e:
            logger.error("Failed to type in input box with %s" % e)
            self.get_windows_img()

    def clear(self, locator):
        el = self.find_element(locator)
        try:
            el.clear()
            logger.info("Clear text in input box before typing.")
        except NameError as e:
            logger.error("Failed to clear in input box with %s" % e)
            self.get_windows_img()

    def click(self, locator):
        el = self.find_element(locator)
        try:
            el.click()
            logger.info("The element \' %s \' was clicked.")
        except NameError as e:
            logger.error("Failed to click the element with %s" % e)

    def get_el_text(self, locator):
        el = self.find_element(locator)
        try:
            return el.text
            logger.info("The element \' %s \' was clicked." % el.text)
        except Exception as e:
            logger.error(
                "Failed to get the text of the element .Reason: %s" % e)

    @property
    def get_page_title(self):
        logger.info("Current page title is %s" % self.driver.title)
        return self.driver.title

    @staticmethod
    def sleep(seconds):
        time.sleep(seconds)
        logger.info("Sleep for %d seconds" % seconds)

    @property
    def collect_handles(self):
        handles = self.driver.window_handles
        logger.info(
            "Have {0} pages are opened,detail handles: {1} ".format(len(handles), handles))
        return handles

    @property
    def current_window(self):
        current_window = self.driver.current_window_handle
        logger.info("Current opened window handle is {}".format(
            current_window))
        return current_window

    def exchange_to_window(self, handle):
        try:
            self.driver.switch_to.window(handle)
            logger.info("Has change to {} window page!".format(handle))
        except Exception:
            logger.error(
                "Current number of windows is only one,unable to exchange!")

    def elements_length(self, locator):
        elements = self.find_elements(locator)
        n = len(elements)
        return n

    @property
    def get_current_url(self):
        return self.driver.current_url

    @property
    def switch_to_altet(self):
        altert = self.driver.switch_to_alert()
        altert.accept()


if __name__ == "__main__":
    p = BasePage()
