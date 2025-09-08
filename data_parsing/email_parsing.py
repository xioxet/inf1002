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
    else:
        plaintext_message = msg.get_content()
   
    returned_msg['plaintext_message'] = plaintext_message

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

def has_url(text): #url detection
    # Multiple patterns to catch different URL formats
    url_patterns = [
        r'https?://[^\s]+',  # Standard http/https URLs
        r'https?:[^\s]+',    # Malformed URLs like https:example.com
        r'\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?',  # Domain names like example.com
        r'www\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?'  # www.example.com
    ]
    
    for pattern in url_patterns:
        if re.search(pattern, text):
            return print('Have URL')
    return print('No URL')
