import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core.tools import mail_env,config,log



class Mailler:

    def __init__(self):
        self.smtp_server = config['smtp']['host']
        self.port = config['smtp']['port']
        self.sender_email = config['smtp']['user']
        self.password = config['smtp']['password']
    
    def __connect(self)->bool:
        try:
            self.context = ssl.create_default_context()
            self.server = smtplib.SMTP(self.smtp_server,self.port)
            self.server.ehlo()
            self.server.starttls(context=self.context) 
            self.server.login(self.sender_email, self.password)
            return True
        except Exception as e:
            log(f"[red][ERROR][MAILLER] Error connecting to server {self.smtp_server}")
            return False

    def send(self,dest,subject,template,data={}):
        message = mail_env.get_template(template+'.html')
        output = message.render(data)
        messageO = MIMEMultipart("alternative")
        messageO["Subject"] = subject
        messageO["From"] = self.sender_email
        messageO["To"] = dest
        part1 = MIMEText(output, "plain")
        part2 = MIMEText(output, "html")
        messageO.attach(part1)
        messageO.attach(part2)
        self.__send(dest,messageO)
    
    def __send(self,dest,message):
        try:
          if self.__connect():
            self.server.sendmail(self.sender_email, dest, message.as_string())
            self.server.quit() 
        except Exception as e:
          log(f"[red][ERROR][MAILLER] Error sending mail {e}")


   