import pandas as pd
import pathlib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import numpy as np
import pickle as pkl
from . import dataset_functions

email_csv_files = [
    {
        'filename': 'CEAS_08.csv',
        'cols': {
            'sender': 'sender',
            'body': 'body',
            'attachments': None,
            'is_phishing': 'label'
        }
    },

    {
        'filename': 'Ling.csv',
        'cols': {
            'sender': None,
            'body': 'body',
            'attachments': None,
            'is_phishing': 'label'
        }
    },

    {
        'filename': 'SpamAssasin.csv',
        'cols': {
            'sender': None,
            'body': 'body',
            'attachments': None,
            'is_phishing': 'label'
        }
    }
]


'''handles serialization to disk'''
def initialize_datasets() -> dict:

    dataset_list = [
        {
            'filename': 'emails',
            'function': dataset_functions.normalize_email_datasets,
            'args': (email_csv_files,)

        },

        {
            'filename': 'keywords',
            'function': dataset_functions.get_keywords,
            'args': ('keyword_dataset.csv',)
        }
    ]

    compiled_datasets = dict()

    for data_dict in dataset_list:
        filepath = pathlib.Path(__file__).parent / 'pickled-datasets' / data_dict['filename']
        if filepath.is_file():
            with open(filepath, 'rb') as file:
                compiled_datasets[data_dict['filename']] = pkl.load(file)
        else:
            dataset = data_dict['function'](*data_dict['args'])
            with open(filepath, 'wb') as file: 
                    pkl.dump(dataset, file)
            compiled_datasets[data_dict['filename']] = dataset

    return compiled_datasets        
