import random
import string
import smtplib,ssl

def code_generaate():
    digits = "".join( [random.choice(string.digits+string.ascii_letters) for i in range(8)] )
    return digits

def send_mail(email):
    print(email)
    otp_code=code_generaate()
    smtp_server='smtp.gmail.com'
    port =587
    sender_email='testmailsocket@gmail.com'
    reciever_email=email
    password='123testmail'
    message="""\
    subject:socket test
    
    your email is been confirmed
    Your otp is -- {}
    """.format(otp_code)
    context=ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server,context=context) as server:
        server.login(sender_email,password)
        server.sendmail(sender_email,reciever_email,message)
    print('send sucessfully')
    return otp_code



code_generaate()