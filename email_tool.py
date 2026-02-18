import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
import getpass

class EmailTool:
    """简单的邮箱工具类"""
    
    def __init__(self):
        self.smtp_server = None
        self.smtp_port = None
        self.imap_server = None
        self.imap_port = None
        self.email = None
        self.password = None
        self.smtp_conn = None
        self.imap_conn = None
    
    def setup(self):
        """配置邮箱信息"""
        print("=" * 50)
        print("邮箱工具配置")
        print("=" * 50)
        
        self.email = input("请输入邮箱地址: ").strip()
        
        # 根据邮箱域名自动配置服务器
        domain = self.email.split('@')[-1].lower()
        
        if domain == 'gmail.com':
            self.smtp_server = 'smtp.gmail.com'
            self.smtp_port = 587
            self.imap_server = 'imap.gmail.com'
            self.imap_port = 993
        elif domain == 'qq.com':
            self.smtp_server = 'smtp.qq.com'
            self.smtp_port = 587
            self.imap_server = 'imap.qq.com'
            self.imap_port = 993
        elif domain == '163.com':
            self.smtp_server = 'smtp.163.com'
            self.smtp_port = 587
            self.imap_server = 'imap.163.com'
            self.imap_port = 993
        elif domain == 'outlook.com' or domain == 'hotmail.com':
            self.smtp_server = 'smtp.office365.com'
            self.smtp_port = 587
            self.imap_server = 'outlook.office365.com'
            self.imap_port = 993
        else:
            print(f"\n未识别到 {domain} 的默认服务器配置")
            self.smtp_server = input("请输入SMTP服务器地址: ").strip()
            self.smtp_port = int(input("请输入SMTP服务器端口 (通常为587或465): ").strip())
            self.imap_server = input("请输入IMAP服务器地址: ").strip()
            self.imap_port = int(input("请输入IMAP服务器端口 (通常为993): ").strip())
        
        self.password = getpass.getpass("请输入邮箱密码/授权码: ")
        print("\n配置完成！\n")
    
    def connect_smtp(self):
        """连接SMTP服务器"""
        try:
            self.smtp_conn = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.smtp_conn.starttls()
            self.smtp_conn.login(self.email, self.password)
            print("SMTP连接成功！")
            return True
        except Exception as e:
            print(f"SMTP连接失败: {e}")
            return False
    
    def connect_imap(self):
        """连接IMAP服务器"""
        try:
            self.imap_conn = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            self.imap_conn.login(self.email, self.password)
            print("IMAP连接成功！")
            return True
        except Exception as e:
            print(f"IMAP连接失败: {e}")
            return False
    
    def send_email(self, to_email, subject, body):
        """发送邮件"""
        if not self.smtp_conn:
            if not self.connect_smtp():
                return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            self.smtp_conn.send_message(msg)
            print("邮件发送成功！")
            return True
        except Exception as e:
            print(f"邮件发送失败: {e}")
            return False
    
    def decode_str(self, s):
        """解码字符串"""
        if not s:
            return ""
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        elif isinstance(value, bytes):
            value = value.decode('utf-8', errors='ignore')
        return value
    
    def fetch_emails(self, count=5):
        """获取最新邮件"""
        if not self.imap_conn:
            if not self.connect_imap():
                return []
        
        try:
            self.imap_conn.select('INBOX')
            _, data = self.imap_conn.search(None, 'ALL')
            email_ids = data[0].split()
            
            emails = []
            # 获取最新的count封邮件
            for i in range(min(count, len(email_ids))):
                email_id = email_ids[-(i + 1)]
                _, msg_data = self.imap_conn.fetch(email_id, '(RFC822)')
                email_body = msg_data[0][1]
                msg = email.message_from_bytes(email_body)
                
                subject = self.decode_str(msg['Subject'])
                from_email = self.decode_str(msg['From'])
                date = msg['Date']
                
                # 获取邮件内容
                content = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            charset = part.get_content_charset() or 'utf-8'
                            content = part.get_payload(decode=True).decode(charset, errors='ignore')
                            break
                else:
                    charset = msg.get_content_charset() or 'utf-8'
                    content = msg.get_payload(decode=True).decode(charset, errors='ignore')
                
                emails.append({
                    'id': email_id.decode(),
                    'subject': subject,
                    'from': from_email,
                    'date': date,
                    'content': content[:500] + '...' if len(content) > 500 else content
                })
            
            return emails
        except Exception as e:
            print(f"获取邮件失败: {e}")
            return []
    
    def close(self):
        """关闭连接"""
        if self.smtp_conn:
            try:
                self.smtp_conn.quit()
            except:
                pass
        if self.imap_conn:
            try:
                self.imap_conn.close()
                self.imap_conn.logout()
            except:
                pass
        print("\n连接已关闭")

def main():
    """主函数"""
    tool = EmailTool()
    
    print("\n" + "=" * 50)
    print("欢迎使用简单邮箱工具")
    print("=" * 50)
    
    tool.setup()
    
    while True:
        print("\n" + "=" * 50)
        print("请选择操作:")
        print("1. 发送邮件")
        print("2. 查看最新邮件")
        print("3. 退出")
        print("=" * 50)
        
        choice = input("请输入选项 (1-3): ").strip()
        
        if choice == '1':
            to_email = input("收件人邮箱: ").strip()
            subject = input("邮件主题: ").strip()
            print("邮件内容 (输入Ctrl+Z或Ctrl+D结束，Windows下按Enter后Ctrl+Z再Enter):")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass
            body = '\n'.join(lines)
            
            tool.send_email(to_email, subject, body)
        
        elif choice == '2':
            count = input("要查看多少封邮件 (默认5): ").strip()
            count = int(count) if count.isdigit() else 5
            
            emails = tool.fetch_emails(count)
            if emails:
                print(f"\n最新 {len(emails)} 封邮件:")
                print("-" * 50)
                for i, email_info in enumerate(emails, 1):
                    print(f"\n【邮件 {i}】")
                    print(f"主题: {email_info['subject']}")
                    print(f"发件人: {email_info['from']}")
                    print(f"日期: {email_info['date']}")
                    print(f"内容预览:\n{email_info['content']}")
                    print("-" * 50)
        
        elif choice == '3':
            tool.close()
            print("再见！")
            break
        
        else:
            print("无效选项，请重新输入！")

if __name__ == "__main__":
    main()
