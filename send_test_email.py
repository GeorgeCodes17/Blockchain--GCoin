import smtplib as smt, ssl
import customer_service_help_password as account_password

def __init__(receiver_email):
    port = 465
    smtp_server = 'smtp.gmail.com'
    password = account_password.__init__()

    receiver_email = receiver_email
    sender_email = 'gcoincustomerhelp24@gmail.com'
    msg = 'GCoin Customer Support- test email [just test not real]'

    try:
        context = ssl.create_default_context()
        with smt.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg)
        print('email sent')
        return True
    except BaseException as b:
        print('email not sent')
        print(b)
        return False

#__init__('georgeosborn2002@gmail.com')