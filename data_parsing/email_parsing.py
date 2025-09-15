import email
from email import policy
from email.parser import BytesParser

from typing import Tuple, BinaryIO
import io, re


''' this is the class that will be fed into the rule based function. all emails, whether or not it's from the .csv or from manual uploading of an .eml file, will be normalised into this class'''
class ProcessedEmail:
    def __init__(self, sender: str, message: str, attachments: list, is_phishing: bool):
        self.sender = sender
        self.message = message
        self.attachments = attachments
        self.is_phishing = None


    '''debugging method, flask gets angry at me because it can't serialise a Python class into json.'''
    def __dict__(self) -> dict:
        return {
            'sender': self.sender,
            'message': self.message,
            'attachments': [file.name for file in self.attachments],
            'is_phishing': None,
        }


''' accepts an .eml file and returns data+metadata.'''
def read_eml(file: BinaryIO) -> ProcessedEmail:
    msg = BytesParser(policy=policy.default).parse(file)
<<<<<<< HEAD
    returned_msg = dict()
    
    # handle multipart emails
    if msg.is_multipart():
        plaintext_message = '\n'.join([msg_part.get_content() for msg_part in msg.walk() if msg_part.get_content_type() == "text/plain"])
        html_message = '\n'.join([msg_part.get_content() for msg_part in msg.walk() if msg_part.get_content_type() == "text/html"])
        
    else:
        
        plaintext_message = msg.get_content() if msg.get_content_type() == "text/plain" else ""
        html_message = msg.get_content() if msg.get_content_type() == "text/html" else ""

    returned_msg['plaintext_message'] = plaintext_message
    returned_msg['html_message'] = html_message
    # isolate attachment
    # i think parsing msg.walk twice is kind of inefficient :s
    # oopsie

=======
 
    msg_parts = []
    msg_body = ''
>>>>>>> 1ce81298caa6f93743b688765f3ebf4c91f388aa
    attachments = []
    
    if msg.is_multipart():
        for msg_part in msg.walk():
            msg_parts.append(msg_part)
    else:
        msg_parts.append(msg)

<<<<<<< HEAD
=======
    for msg_part in msg_parts:
        print(msg_part.get_content_disposition)
        if 'text' in msg_part.get_content_type():
            msg_body += msg_part.get_content()   

        # handles attachments
        if msg_part.get_content_disposition() == "attachment":
            filedata = msg_part.get_payload(decode=True)
            file_obj = io.BytesIO(filedata)
            file_obj.name = msg_part.get_filename()
            attachments.append(file_obj)
    
    
    return ProcessedEmail(
            msg['from'],
            msg_body,
            attachments,
            None
    )

>>>>>>> 1ce81298caa6f93743b688765f3ebf4c91f388aa


def url_detection(text): #url detection
    # Multiple patterns to catch different URL formats
    url_patterns = [
        # 1) Schemed URLs (http/https/ftp) incl. auth, IPv4/IPv6, localhost, port, path
        r'(?:https?|ftp)://(?:[^\s:@/]+(?::[^\s:@/]*)?@)?(?:(?:[a-z0-9-]+\.)+(?:[a-z]{2,63}|xn--[a-z0-9-]+)|localhost|\d{1,3}(?:\.\d{1,3}){3}|\[(?:[0-9a-f:.]+)\])(?::\d{2,5})?(?:/[^\s<>()\[\]{}"\']*)?',
        # 2) www.* without scheme
        r'www\.(?:[a-z0-9-]+\.)+(?:[a-z]{2,63}|xn--[a-z0-9-]+)(?::\d{2,5})?(?:/[^\s<>()\[\]{}"\']*)?',
        # 3) bare domain (no scheme/www), optional port+path; avoid emails & scheme/www overlaps
        r'(?<!@)(?<!://)(?<!www\.)(?:[a-z0-9-]+\.)+(?:[a-z]{2,63}|xn--[a-z0-9-]+)(?::\d{2,5})?(?:/[^\s<>()\[\]{}"\']*)?',
        # 4) scheme without // (e.g., https:example.com)
        r'(?:https?|ftp):(?!//)[^\s<>()\[\]{}"\']+'
    ]

    for pattern in url_patterns:
        if re.findall(pattern, text):
            url_link = re.findall(pattern,text)
            print(url_link)
            #all urls will be stored in list.
            return url_link
    print('No Url Detected')
    return False

#def url_analyzer(url):
    #Identify links that do not match the claimed domain or contain IP addresses instead of domains.
