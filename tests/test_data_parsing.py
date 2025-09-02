import pytest
import pathlib
from data_parsing import read_eml


def test_read_eml():
    filepath = pathlib.Path(__file__).parent / "testfiles" / "test_email.eml"
    eml_file = open(filepath, 'rb')
    print(read_eml(eml_file))

test_read_eml()
