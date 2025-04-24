import smtplib
import os
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
    # 从环境变量获取配置
    ZOTERO_ID = os.environ.get("ZOTERO_ID")
    ZOTERO_KEY = os.environ.get("ZOTERO_KEY")
    
    # SMTP服务器信息
    SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.163.com")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "25"))
    SMTP_USERNAME = os.environ.get("SMTP_USERNAME")
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
    EMAIL_FROM = os.environ.get("EMAIL_FROM")
    EMAIL_TO = os.environ.get("EMAIL_TO")

    # 验证必要的环境变量是否存在
    required_vars = {
        "ZOTERO_ID": ZOTERO_ID,
        "ZOTERO_KEY": ZOTERO_KEY,
        "SMTP_USERNAME": SMTP_USERNAME,
        "SMTP_PASSWORD": SMTP_PASSWORD,
        "EMAIL_FROM": EMAIL_FROM,
        "EMAIL_TO": EMAIL_TO
    }

    missing_vars = [var for var, value in required_vars.items() if not value]
    if missing_vars:
        raise ValueError(f"缺少必要的环境变量: {', '.join(missing_vars)}")

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
    