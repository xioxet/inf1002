import pandas as pd
import pathlib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import numpy as np
import pickle as pkl

from . import dataset_functions

'''handles serialization to disk'''
def initialize_datasets() -> dict:
    
    # we only have one such function that requires ml for now, bu if we need any in the future, we just add to this list! :)
    # given the ml operations are damn expensive, we really only want to compute them once.

    dataset_list = [
        {
            'filename': 'keywords',
            'function': dataset_functions.get_keywords,
            'args': ('test_dataset.csv',)
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

# meant for global access, so we capitalize ^_^
COMPILED_DATASETS = initialize_datasets()

