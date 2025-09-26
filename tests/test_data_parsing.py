import pytest
import pathlib
import hashlib
from data_parsing import read_eml
from utils import *

def test_read_eml():
    filepath = current_filepath(__file__) / "testfiles" / "test_email.eml"
    eml_file = open(filepath, 'rb')
    parsed_eml = read_eml(eml_file)

    assert parsed_eml['plaintext_message'] == 'This is an HTML message. Please use an HTML capable mail program to read\nthis message.\n\nThis is just a plain text attachment file named attachment.txt .'

    assert '1f209f1560df8cb6e983dff99d7a7d2db8dc3e439226abd38ef34facdffd82ec' == hashlib.sha256(parsed_eml['attachments'][0].read()).hexdigest()

