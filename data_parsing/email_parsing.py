import email
from email import policy
from email.parser import BytesParser

from typing import Tuple, BinaryIO
import io, re

''' accepts an .eml file and returns data+metadata.'''
def read_eml(file: BinaryIO) -> dict:
    msg = BytesParser(policy=policy.default).parse(file)
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

    attachments = []
    for part in msg.walk():
        if part.get_content_disposition() == "attachment":
            filedata = part.get_payload(decode=True)
            file_obj = io.BytesIO(filedata)
            file_obj.name = part.get_filename()
            attachments.append(file_obj)
    returned_msg['attachments'] = attachments
    
    return returned_msg



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
