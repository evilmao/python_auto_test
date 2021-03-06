# -*- coding:utf-8 -*-
# author by Failymao
"""
- 封装的选择浏览器、打开网址的类
"""
from functools import wraps
import os
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from src.utils.config import DRIVER_PATH, REPORT_PATH
from src.utils.log import logger


# 对应浏览器下的驱动
CHROMEDRIVER_PATH = DRIVER_PATH + '\chromedriver.exe'
FIREDRIVER_PATH = DRIVER_PATH + '\geckodriver.exe'
PHANTOMJSDRIVER_PATH = DRIVER_PATH + '\phantomjs.exe'
IEDRIVER_PATH = DRIVER_PATH + '\IEDriverServer.exe'

TYPES = {'firefox': webdriver.Firefox,
         'chrome': webdriver.Chrome,
         'phantomjs': webdriver.PhantomJS,
         'ie': webdriver.Ie
         }
EXECUTABLE_PATH = {'firefox': FIREDRIVER_PATH,
                   'chrome': CHROMEDRIVER_PATH,
                   'phantomjs': PHANTOMJSDRIVER_PATH,
                   'ie': IEDRIVER_PATH

                   }


class UnSupportBrowserTypeError(Exception):  # 自定义错误类
    pass


class Browser(object):
    '''Browser Type.'''

    def __init__(self, browser_type='firefox'):
        self._type = browser_type.lower()  # 浏览器名字私有属性
        if self._type in TYPES:
            self.browser = TYPES[self._type]
            logger.info('Yod had select {} browser.'.format(self._type))
            if self._type == 'phantomjs':
                SERVICE_ARGS = ['--load-images=true',
                                '--disk-cache=true'
                                ]
                self.driver = self.browser(
                    executable_path=EXECUTABLE_PATH[self._type], service_args=SERVICE_ARGS)
            self.driver = self.browser(
                executable_path=EXECUTABLE_PATH[self._type])

        else:
            raise UnSupportBrowserTypeError('仅支持%s!' % ', '.join(TYPES.keys()))
            self.driver = None
            logger.Error('仅支持%s！检测浏览器拼写！' % ', '.join(TYPES.keys()))

    def open_browser(self, url, maximize_window=True, implicitly_wait=5):  # 打开指定网址
        driver = self.driver
        logger.info("Starting {} browser.".format(self._type))
        driver.get(url)
        logger.info("The test server url is: {}".format(url))
        if maximize_window:
            driver.maximize_window()
            logger.info("Maximize the current window.")
        driver.implicitly_wait(implicitly_wait)
        logger.info("Set implicitly wait {} seconds.".format(implicitly_wait))
        return driver

    def close(self):
        self.driver.close()

    def quit(self):
        logger.info("Now, Close and quit the browser.")
        self.driver.quit()


class Screen(object):
    '''单独封装一个截图功能的类'''
    flag = 'IMAGE'

    def __init__(self, driver):
        self.driver = driver

    def _screenshot(self, name):
        day = time.strftime('%Y%m%d', time.localtime(time.time()))
        screen_name = name + '.PNG'
        path = REPORT_PATH + '\screenshot_%s' % day
        if not os.path.exists(path):
            os.makedirs(path)
        self.driver.save_screenshot(path + '\\%s' % screen_name)
        return screen_name

    def __call__(self, test_func):
        @wraps(test_func)
        def wrapper(*args):
            try:
                return test_func(*args)
            except WebDriverException:
                raise WebDriverException(
                    message=self.flag + self._screenshot(test_func.__qualname__))

        return wrapper



#-----------------------测试---------------
if __name__ == '__main__':
    b = Browser(browser_type='chrome').open_browser('http://www.baidu.com')
    # b.save_screen_shot('test_baidu')
    time.sleep(3)
    b.quit()
