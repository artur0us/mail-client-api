import smtplib, re
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

class MBoxSendersEntity:

  @staticmethod
  def send_email(msg_from, msg_to, msg_subj, body_text, files = None, mail_server_host = '0.0.0.0'):
    # Return: bool(function execution flag), str(reason message)

    # Usage:
    # send_email("from@domain.domain", ["recepient@domain.domain"], "Subject text", "Body text", [], "0.0.0.0")

    ###################
    # Base checks
    ###################
    # *From* field
    if type(msg_from) != str:
      return False, "Wrong *from* field variable type!"
    if ("@" not in msg_from) and ("." not in msg_from):
      return False, "*From* field is not specified!"
    if len(msg_from) < 4:
      return False, "*From* field is too short!"
    # *To* field
    if type(msg_to) != list:
      return False, "Wrong *To* field variable type!"
    if len(msg_to) < 1:
      return False, "*To* field is empty!"
    for one_to_field in msg_to:
      if ("@" not in one_to_field) and ("." not in one_to_field):
        return False, "*To* field is not specified!"
      if len(one_to_field) < 4:
        return False, "*To* field is too short!"
    # *Subject* field
    if type(msg_subj) != str:
      return False, "Wrong *Subject* field variable type!"
    if msg_subj == "":
      return False, "*Subject* field is empty!"
    # *Text body* field
    if type(body_text) != str:
      return False, "Wrong *Text body* field variable type!"
    # if body_text == "":
    #   return False, "*Text body* field is empty!"
    # Mail server host
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", mail_server_host) == None:
      # Domain name is detected
      if len(mail_server_host) < 1:
        return False, "Incorrect mail server host!"
    # Files
    if (files != None) and (type(files) == list):
      for one_file in files:
        if type(one_file) != str:
          return False, "Wrong attachment variable type!"

    # Base parameters
    msg = MIMEMultipart()
    msg['From'] = msg_from
    msg['To'] = COMMASPACE.join(msg_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = msg_subj
    msg.attach(MIMEText(body_text))

    # Email messages attachments
    for one_file in files or []:
      with open(one_file, "rb") as fil:
        part = MIMEApplication(
          fil.read(),
          Name=basename(one_file)
        )
      part['Content-Disposition'] = 'attachment; filename="%s"' % basename(one_file)
      msg.attach(part)

    # SMTP connection and email sending
    smtp = smtplib.SMTP(mail_server_host)
    smtp.sendmail(msg_from, msg_to, msg.as_string())
    smtp.close()
    return True, "ok"