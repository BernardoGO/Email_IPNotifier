import socket
import fcntl
import struct
import os

__LAST_IP_FILE__ = 'lastip.dat'
__PASSWORD_FILE__ = 'sensiveEmailPassword.dat' #A separated file is necessary in order to use gitignore

#enxfc8fc4081bee
__NETWORK_DEVICE__ = 'enp3s0f1'

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
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])
    except:
        return ""

if not os.path.exists(__LAST_IP_FILE__):
    file_ = open(__LAST_IP_FILE__, 'w')
    file_.write("")
    file_.close()

if not os.path.exists(__PASSWORD_FILE__):
    file_ = open(__PASSWORD_FILE__, 'w')
    file_.write("")
    file_.close()

ip = get_ip_address(__NETWORK_DEVICE__)

infile = open(__LAST_IP_FILE__, 'r')
firstLine = infile.readline()
infile.close()

infile = open(__PASSWORD_FILE__, 'r')
password = infile.readline()
infile.close()

if firstLine != ip:
    file_ = open(__LAST_IP_FILE__, 'w')
    file_.write(str(ip))
    file_.close()
    send_email("bernardo.godinho.oliveira@gmail.com", #you should not hardcode things
                password,
                "bernardo.godinho.oliveira@gmail.com",
                "IP CHANGED",
                str(ip));
    print "different"
else:
    print "equal"
