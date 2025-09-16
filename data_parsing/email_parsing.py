import email
from email import policy
from email.parser import BytesParser
from typing import Tuple, BinaryIO
import io


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


    msg_parts = []
    msg_body = ''

    attachments = []
    
    if msg.is_multipart():
        for msg_part in msg.walk():
            msg_parts.append(msg_part)
    else:
        msg_parts.append(msg)


    for msg_part in msg_parts:
        #print(msg_part.get_content_disposition)
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


