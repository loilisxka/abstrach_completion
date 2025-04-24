# Zotero 摘要自动补全工具

这个工具可以自动补全 Zotero 库中缺失的文献摘要，并通过邮件通知补全结果。

## 功能

- 自动检查并补全 Zotero 库中缺失的摘要
- 通过邮件通知补全结果
- 支持 GitHub Actions 自动运行

## 配置说明

1. Fork 这个仓库到你的 GitHub 账号下

2. 在仓库的 Settings -> Secrets and variables -> Actions 中添加以下 secrets：

   - `ZOTERO_ID`: 你的 Zotero 用户 ID
   - `ZOTERO_KEY`: 你的 Zotero API Key
   - `SMTP_SERVER`: SMTP 服务器地址（默认为 smtp.163.com）
   - `SMTP_PORT`: SMTP 服务器端口（默认为 25）
   - `SMTP_USERNAME`: SMTP 用户名
   - `SMTP_PASSWORD`: SMTP 密码
   - `EMAIL_FROM`: 发件人邮箱
   - `EMAIL_TO`: 收件人邮箱

3. GitHub Actions 将会：
   - 每天自动运行一次
   - 可以手动触发运行
   - 运行完成后发送邮件通知结果

## 手动运行

如果你想手动运行这个工具，可以：

1. 克隆仓库
2. 安装依赖：`pip install -r requirements.txt`
3. 设置环境变量
4. 运行脚本：`python zotero_abstract_completion.py`
