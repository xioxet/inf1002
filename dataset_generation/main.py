import pandas as pd
import pathlib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import numpy as np
import pickle as pkl
from . import dataset_functions
import json

'''handles serialization to disk'''
def initialize_datasets() -> dict:
    
    with open(pathlib.Path(__file__).parent / 'datasets' / 'emails' / 'metadata.json') as f:
        email_csv_files = json.load(f)

    with open(pathlib.Path(__file__).parent / 'datasets' / 'domains' / 'metadata.json') as f:
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
        filepath = pathlib.Path(__file__).parent / 'pickled-datasets' / data_dict['filename'] + '.pkl'
        if filepath.is_file():
            with open(filepath, 'rb') as file:
                compiled_datasets[data_dict['filename']] = pkl.load(file)
        else:
            # lazy evaluation is necessary here
            args = data_dict['args']()
            dataset = data_dict['function'](*args)
            with open(filepath, 'wb') as file: 
                    pkl.dump(dataset, file)
            compiled_datasets[data_dict['filename']] = dataset

    return compiled_datasets        
