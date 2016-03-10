import socket
import fcntl
import struct
import os

def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, TO, message)
    server.close()
    print 'successfully sent the mail'

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

if not os.path.exists('lastip.dat'):
    file_ = open('lastip.dat', 'w')
    file_.write("")
    file_.close()
ip = get_ip_address('enp3s0f1')#enxfc8fc4081bee
infile = open('lastip.dat', 'r')
firstLine = infile.readline()
infile.close()
if firstLine != ip:
    file_ = open('lastip.dat', 'w')
    file_.write(str(ip))
    file_.close()
    print "different"
else:
    print "equal"



##send_email("bernardo.godinho.oliveira@gmail.com", "xxxx", "bernardo.godinho.oliveira@gmail.com", "IP ACK", "test");
