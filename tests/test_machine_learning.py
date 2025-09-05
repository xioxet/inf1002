import pytest
import pathlib

from machine_learning import *

def test_get_keywords():
    assert get_keywords('test_dataset.csv')
