import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from zotero_abstract_completer import ZoteroAbstractCompleter

# 邮件发送函数
def send_email(subject, body, smtp_server, smtp_port, smtp_username, smtp_password, email_from, email_to):
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(email_from, email_to, msg.as_string())
        print(f"邮件已发送到 {email_to}")
    except Exception as e:
        print(f"发送邮件时出错: {e}")


def main():
    # 在这里填写你的Zotero信息
    ZOTERO_ID = "16076403"
    ZOTERO_KEY = "ETem7u5Vn5TAVNARb6Djj4Kq"
    
    # SMTP服务器信息
    SMTP_SERVER = "smtp.163.com"
    SMTP_PORT = 25
    SMTP_USERNAME = "18357457736@163.com"
    SMTP_PASSWORD = "TBqvG34Ck9ePh5vn"
    EMAIL_FROM = "18357457736@163.com"
    EMAIL_TO = "2507608782@qq.com"

    completer = ZoteroAbstractCompleter(ZOTERO_ID, ZOTERO_KEY)
    try:
        completer.complete_abstracts()
        subject = "Zotero摘要补全成功"
        body = "所有缺失的摘要已成功补全。"
    except Exception as e:
        subject = "Zotero摘要补全失败"
        body = f"摘要补全过程中出现错误: {e}"

    send_email(subject, body, SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, EMAIL_FROM, EMAIL_TO)


if __name__ == "__main__":
    main() 
    