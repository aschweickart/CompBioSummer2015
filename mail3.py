#!/usr/local/bin/python

import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import COMMASPACE, formatdate
from email import encoders


def send_mail(send_from, send_to, subject, text, zipfile,
    server="smtp.cs.hmc.edu"):
    assert isinstance(send_to, list)
    msg = MIMEMultipart(
        Subject=subject,
        From=send_from,
        To=COMMASPACE.join(send_to),
        Date=formatdate(localtime=True),
    )
    msg.attach(MIMEText(text))           
    themsg = MIMEBase('application', 'zip')
    zf = open(zipfile, 'r')
    themsg.set_payload(zf.read())
    zf.close()
    encoders.encode_base64(msg)
    themsg.add_header('Content-Disposition', 'attachment', filename=file+'.zip')
    msg.attach(themsg)


    # for f in files or []:
    #     with open(f, "rb") as fil:
    #         msg.attach(MIMEApplication(
    #             fil.read(),
    #             Content_Disposition='attachment; filename="%s"' %basename(f)
    #         ))

    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()
