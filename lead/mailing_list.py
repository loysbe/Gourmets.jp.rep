import smtplib
import ssl
import email.message
import email.mime.*

# help(smtplib)

# gmail API part
# clientID = 976806583305-dp1aafcb5ttq5pp93032sls00t25rb3k.apps.googleusercontent.com


smtp_server = 'smtp.gmail.com'
port = 465
ltd_japon_id = 'loys.belleguie@ltd-japon.com'
password = 'xxxxxxx'

email_content = "Message body"
list_of_email = ['blgl@outlook.jp']
# Enter Email list here

msg = email.message.Message()
msg['Subject'] = 'Subject of Email'
msg['From'] = 'contact@ltd-japon.com'
# create app password in accounts/security
msg.add_header('Content-Type', 'text/html')
msg.set_payload(email_content)


def send_email_587():
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()

    # Login Credentials for sending the mail
    s.login(ltd_japon_id, password)

    for dest in list_of_email:
        s.sendmail(msg['From'], dest, msg.as_string())
        print(f"sending to {dest}")
    
    s.quit()
    return

def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}

def create_message_with_attachment(
    sender, to, subject, message_text, file):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file: The path to the file to be attached.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  content_type, encoding = mimetypes.guess_type(file)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
    fp = open(file, 'rb')
    msg = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(file, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(file, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(file, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()
  filename = os.path.basename(file)
  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  return {'raw': base64.urlsafe_b64encode(message.as_string())}


def send_email():

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(ltd_japon_id, password)
        server.sendmail(msg['From'], list_of_email[0], msg.as_string())
        server.quit()

    return


if __name__ == '__main__':
    send_email()
