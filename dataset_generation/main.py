import pandas as pd
import pathlib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import numpy as np
import pickle
from . import dataset_functions
import json
import copy
from utils import *

'''handles serialization to disk'''
def initialize_datasets() -> dict:
    
    with open(current_filepath(__file__) / 'datasets' / 'emails' / 'metadata.json') as f:
        email_csv_files = json.load(f)

    with open(current_filepath(__file__) / 'datasets' / 'domains' / 'metadata.json') as f:
        domain_files = json.load(f)

    compiled_datasets = {}

    dataset_list = [
        {
            'filename': 'emails',
            'function': dataset_functions.normalize_email_datasets,
            'args': lambda: (email_csv_files,)

        },

        {
            'filename': 'keywords',
            'function': dataset_functions.get_keywords,
            'args': lambda: (compiled_datasets['emails'],)
        },

        {
            'filename': 'domains',
            'function': dataset_functions.normalize_domain_datasets,
            'args': lambda: (domain_files,)
        }
    ]


    for data_dict in dataset_list:
        filepath = (current_filepath(__file__) / 'pickled-datasets' / data_dict['filename']).with_suffix('.pkl')
        if filepath.is_file():
            print(f'{data_dict["filename"]} already saved to disk!')
        else:
            # lazy evaluation is necessary here
            print(f'{data_dict["filename"]} not saved to disk. generating from scratch - this might take a while...')
            args = data_dict['args']()
            dataset = data_dict['function'](*args)
            with open(filepath, 'wb') as file: 
                    pickle.dump(dataset, file)

        compiled_datasets[data_dict['filename']] = filepath 

    return compiled_datasets
