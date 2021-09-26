import smtplib as smt, random
import customer_service_help_password as password
from email.message import EmailMessage

def smtp_connection(receiver_email, password, verification_code):
    port = 465
    smtp_server = 'smtp.gmail.com'
    password = password.__init__()

    #  Just for testing
    Subject: 'GCoin Customer Support'
    receiver_email = receiver_email
    sender_email = "gcoincustomerhelp24@gmail.com"

    msg = EmailMessage()
    msg.set_content("You recently requested a verification code to change your passnumber"\
     + '\n'*2 + "Verification code to change GCoin password is "\
     + verification_code + "." + '\n'*3 + 'Wishing you many GCoin,' + '\n' +\
     'The Customer Service Team.' + '\n'*2 + 'This message was sent with Python')
    msg['Subject'] = 'GCoin Customer Support'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        #  Create a secure SSL context
        with smt.SMTP_SSL(smtp_server, port) as server:
            server.login(sender_email, password)
            server.send_message(msg)
        return True
    except BaseException:
        return False

#  Just for check it works
#smtp_connection('georgeosborn2002@gmail.com', password)
