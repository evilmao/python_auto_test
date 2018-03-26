# -*- coding:utf-8 -*-
# author by Failymao

'''
- 封装logging库，使框架可以很简单地打印日志（输出到控制台以及日志文件）
'''
import logging
from logging.handlers import TimedRotatingFileHandler
from src.utils.config import LOG_PATH, Config


class Logger(object):
    def __init__(self, logger_name='framework'):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)
        c = Config().get('log')  # log_dir

        self.log_file_name = c.get('file_name') if c and c.get(
            'file_name') else 'XSTZ_WAP.log'  # 日志文件

        self.backup_count = c.get('backup') if c and c.get(
            'backup') else 5  # 保留的日志数量
        # 日志输出级别
        self.console_output_level = c.get('console_level') if c and c.get(
            'console_level') else 'WARNING'
        self.file_output_level = c.get(
            'file_level') if c and c.get('file_level') else 'DEBUG'

        # 日志输出格式
        pattern = c.get('pattern') if c and c.get(
            'pattern') else '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

        self.formatter = logging.Formatter(pattern)

    def get_logger(self):
        if not self.logger.handlers:  # 避免重复日志
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)

            # 每天重新创建一个日志文件，最多保留backup_count份
            file_handler = TimedRotatingFileHandler(filename=LOG_PATH + '\\' + self.log_file_name,
                                                    when='D',
                                                    interval=1,
                                                    backupCount=self.backup_count,
                                                    delay=True
                                                    )

            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)
        return self.logger


logger = Logger().get_logger()
