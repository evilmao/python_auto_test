# -*- coding:utf-8 -*-
# author by Failymao

"""
邮件类。用来给指定用户发送邮件。可指定多个收件人，可带附件。
"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import smtplib
from socket import gaierror, error
from src.utils.log import logger


class Email:
    def __init__(self, HOST, sender, password, receiver, title, message=None, path=None):
        """
                    初始化Email
        :param title: 邮件标题，必填。
        :param message: 邮件正文，非必填。
        :param path: 附件路径，可传入list（多附件）或str（单个附件），非必填。
        :param HOST: smtp服务器，必填。
        :param sender: 发件人，必填。
        :param password: 发件人密码，必填。
        :param receiver: 收件人，多收件人用“；”隔开，必填。
        """
        self.title = title
        self.message = message
        self.files = path
        self.msg = MIMEMultipart('related')
        self.HOST = HOST
        self.sender = sender
        self.receiver = receiver
        self.password = password

    def _attach_file(self, att_file):  # 将单个文件添加到附件列表中
        f = open(att_file, "rb")
        mail_body = f.read()
        f.close
        att = MIMEText(mail_body, 'plain', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'

        file_name = re.split(r'[\\|/]', att_file)
        att["Content-Disposition"] = 'attachment; filename="%s"' % file_name[-1]
        self.msg.attach(att)
        logger.info('attach file {}'.format(att_file))

    def send(self):
        self.msg['Subject'] = self.title
        self.msg['From'] = self.sender
        self.msg['To'] = self.receiver

        # 邮件正文
        if self.message:
            self.msg.attach(MIMEText(self.message, "html", 'utf-8'))

        # 添加附件，支持多个附件（传入list），或者单个附件（传入str）
        if self.files:
            if isinstance(self.files, list):
                for f in self.files:
                    self._attach_file(f)
            elif isinstance(self.files, str):
                self._attach_file(self.files)  # 将实例化中的path作为参数传递给实例化方法

        # 连接服务器并发送
        try:
            server = smtplib.SMTP(self.HOST, "25")  # 连接sever

        except (gaierror and error) as e:
            logger.exception('发送邮件失败,无法连接到SMTP服务器，检查网络以及SMTP服务器. %s', e)
        else:
            try:
                server.login(self.sender,
                             self.password
                             )  # 登录

            except smtplib.SMTPAuthenticationError as e:
                logger.exception('用户名密码验证失败！%s', str(e))
                pass
            else:
                server.sendmail(self.sender,               # FROM
                                self.receiver.split(';'),  # TO
                                self.msg.as_string()       # message
                                )  # 发送邮件
                logger.info('发送邮件"{0}"成功! 收件人：{1}。如果没有收到邮件，请检查垃圾箱，'
                            '同时检查收件人地址是否正确'.format(self.title, self.receiver))
                print('Email send success!')
        finally:
            server.quit()  # 断开连接
