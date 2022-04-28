import json
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Gmail(object):
    # =============================================================================
    # SEND EMAIL FUNCTION
    # =============================================================================
    def send_email(self, gpass, sent_to, sent_subject, sent_body):
        sender_email ='dailataranjan@gmail.com'
        receiver_email = sent_to
        password = gpass
        
        message = MIMEMultipart("alternative")
        message["Subject"] = sent_subject
        message["From"] = sender_email
        message["To"] = receiver_email
        
        # Create the plain-text and HTML version of your message
        text = sent_body
        html = f"""\
        <html>
          <body>
            <p>
                {sent_body}
            </p>
          </body>
        </html>
        """
        
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        
        message.attach(part1)
        message.attach(part2)
    
        try:
            ssl_context = ssl.create_default_context()
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl_context)
            server.ehlo()
            server.login(sender_email, password)  
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.close()
            print('Email sent!')
        except Exception as exception:
            print("Error: %s!\n\n" % exception)
    # =============================================================================
    # END OF SEND EMAIL FUNCTION
    # =============================================================================