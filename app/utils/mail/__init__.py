import smtplib
from email.mime.text import MIMEText
from email.header import Header

'''class SendMessage:
    def __init__(self, ):
        return

    def send(self, to_msg, to_add):
        mail_host = "smtp.163.com"  # 设置服务器
        mail_user = "chenyong76130@163.com"  # 用户名
        mail_pass = "cy123123"  # 口令
        sender = 'chenyong76130@163.com'
        receivers = [to_add]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        conten = to_msg
        message = MIMEText(conten, 'plain', 'utf-8')
        message['From'] = "chenyong76130@163.com"
        message['To'] = to_add
        subject = '商家新闻处理'
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException as e:
            print("Error: 无法发送邮件" + e.strerror)

def main():
    sender = SendMessage()
    sender.send('请尽快审核商家所发布的广告', 'jlgnfdljbjvkd@foxmail.com')'''
