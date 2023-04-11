from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient import errors

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from base64 import urlsafe_b64encode

import sys
import csv

address = {}

ltd_japon_id = 'loys.belleguie@ltd-japon.com'
# password = 'xxxxx'

def create_message(sender, to, cc,  bcc, subject, message_text):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEMultipart()
    message['To'] = to
    message['Bcc'] = bcc
    message['From'] = sender
    message['subject'] = subject

    message.attach(MIMEText(message_text + '<p><a href="https://www.gourmets.jp/mailing_list_B2B"><img src="cid:image1" /></a></p>', 'html'))

    # This example assumes the image is in the current directory
    fp = open('.\lead\offre_foie_gras.jpg', 'rb')
    image = MIMEImage(fp.read())
    fp.close()
    # image.seek(0)
    # img = MIMEImage(image.read(), 'png')
    image.add_header('Content-Id', '<image1>')
    image.add_header("Content-Disposition", "inline", filename="image1")
    message.attach(image)

    return {'raw': urlsafe_b64encode(message.as_bytes()).decode("utf-8")}
    # return message

def create_message_with_attachment(sender, to, subject, message_text, file):
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

def send_message(service, user_id, message):
    """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
    try:
        m = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % m['id'])
        return m
    except errors.HttpError as e:
        print ('An error occurred:', e)

def set_send_alias(service,alias_name):
    
    aliases = service.users().settings().sendAs().list(userId=ltd_japon_id).execute()
    for alias in aliases.get('sendAs'):
        if (alias.get('sendAsEmail') == alias_name):
            print(alias)
            break

    sendAsConfiguration = {"sendAsEmail": alias_name,
        "isDefault": True,
        "replyToAddress": alias_name,
        "displayName": "Gourmets jp",
        "isPrimary": False,
        "treatAsAlias": False,
        'signature': 'www.gourmets.jp'
        }
    result = service.users().settings().sendAs().patch(userId=ltd_japon_id,sendAsEmail=alias_name,body=sendAsConfiguration).execute()
    # result = service.users().settings().sendAs().create(userId=ltd_japon_id,body=sendAsConfiguration).execute()
    print ('Updated signature for: %s' % result.get('displayName'))

def getAddresses(fichier):
    global address
    f = open(fichier, 'r',encoding='utf-8')
    add = f.readlines()
    f.close()
    already_done = []
    i=0

    with open(fichier, newline='',encoding='utf-8') as csvfile:
        add = csv.reader(csvfile, delimiter=',', quotechar='\"')
        for b in add:
            if ( b[6] != ''):
                if ( b[7] == '1' ):
                    already_done.append(b[6])
                if ( b[6] not in already_done ):
                    print(b[6], i)
                    i+=1
                    address[b[0]] = b[6]
        print(len(address),' emails')
    csvfile.close()
    return
    for a in add[1:len(add)]:
        b = a.split(',')
        # print(b[0],b[6])
        if ( b[6] != ''):
            if ( b[7] == '1' ):
                already_done.append(b[6])
            if ( b[6] not in already_done ):
                print(b[6], i)
                i+=1
                address[b[0]] = b[6]
    print(len(address),' emails')
    return

import time
def send_mailing():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    scopes = ['https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.settings.sharing',
    'https://www.googleapis.com/auth/gmail.settings.basic']

    service = connect(scopes)
    
    subject = '【業務用限定 Promotion】フランス産 フォアグラ・鴨肉「IGP」お見逃しなく！'
    # list_of_email = {'a':'blgl@outlook.jp','b':'jetestetout@live.fr'}
    list_of_email = {'b':'blgl@outlook.jp'}
    # list_of_email = address
    email_content = make_email()
    sender = 'Gourmets.jp@ltd-japon.com'

    i = 0
    for name in list_of_email:
        i += 1
        print(i, ' : sending mail to :', name, list_of_email[name])
        text = name + ' 様<br>' + email_content
        message = create_message(sender, list_of_email[name], '', 'Gourmets.jp@ltd-japon.com', subject, text)
        send_message(service, ltd_japon_id, message)
        # wait 
        time.sleep(2)

def make_email() -> str :
    s = 'フランス産 食品輸入の グルメ・ジャポンと申します。<br> \
        <a href="https://www.gourmets.jp">www.gourmets.jp</a>は個人経営、高級食品輸入・通販サイトです。<br>\
         原産地（フランス）のメーカーと、特別なお付き合いを築き、日本のお客様へ厳選食材をご提案致します。<br>\
        <strong>この度は、年末年始向け、フォアグラのプロモーションをご提案させていただきます。</strong><br> \
        <p>是非ご検討下さい！ <a href="https://www.gourmets.jp/mailing_list_B2B">詳細はこちら！</a><br> Tel : 080-3724-2301</p>'
    return s

def connect(scopes):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('.\lead\gmailAPI_credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def test():
    # Call the Gmail API
    # If modifying these scopes, delete the file token.pickle.
    scopes = ['https://www.googleapis.com/auth/gmail.readonly']
    service = connect(scopes)
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])
    # service.quit()

if __name__ == '__main__':
    # test()
    # fichier = r'.\lead\lead_french2.csv' 
    fichier = r'.\lead\lead_french_sending.csv' 
    getAddresses(fichier)
    send_mailing()
