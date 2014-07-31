import smtplib
from email.mime.text import MIMEText
import os
from bs4 import BeautifulSoup
from config import SITE_DOMAIN

class mail:
    def __init__(self):
        # mail server details
        self.me = 'noreply@' + SITE_DOMAIN
        self.password = "noreplypassword"
        self.mail_server = SITE_DOMAIN

    def send_forgot_password(self, to, link):
        # read template from file
        fp = open(os.path.dirname(os.path.realpath(__file__)) + "/templates/forgot_password.html", 'rb')
        html = fp.read()
        fp.close()
        
        # add links
        soup = BeautifulSoup(html)
        site_url = 'https://' + SITE_DOMAIN
        new_link = site_url + '/passwordreset/' + link
        soup.find(text="site_url").replaceWith(site_url)
        for a in soup.findAll('a'):
            a['href'] = a['href'].replace("site_url", site_url)
            a['href'] = a['href'].replace("forgot_password_link", new_link)
        html = str(soup)
        
        # send mail
        msg = MIMEText(html, 'html')
        msg['Subject'] = 'Password Reset for ' + site_url
        msg['From'] = self.me
        msg['To'] = to
        result = "password reset link sent."
        try:
            s = smtplib.SMTP(self.mail_server)
            s.login(self.me, self.password)
            s.sendmail(self.me, [to], msg.as_string())
            s.quit()
        except smtplib.SMTPException, e:
            result = "SMTPException " + str(e)
        except smtplib.socket.error, e:
            result = "smtplib.socket.error " + str(e)
        return result
        
        
        
