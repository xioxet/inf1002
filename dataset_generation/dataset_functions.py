import pandas as pd
import pathlib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import numpy as np
import pickle as pkl

'''
so unfortunately, bc we are gathering from different datasets
the names and labels of things are not going to be standardised

sender (str)
body (str)
attachments (list)
is_phishing (bool)

functionally this is just going to be a dict of dicts that we can happy happy join together

some lack the information that we're actually looking for
but this is Ok because this is just for training purposes

this is written with the future in mind: if we need more datasets, we just add it to this list!
'''
def normalize_email_datasets(email_csv_files: list) -> dict:
    
    datasets = []
    
    for f in email_csv_files:
        file = pathlib.Path(__file__).parent / 'datasets' / 'emails' / f['filename']
        print(file)
        dataset = pd.read_csv(pathlib.Path(__file__).parent / 'datasets' / 'emails' / f['filename'])
        for col in f['cols']:
            if f['cols'][col] is not None: 
                dataset.rename(columns={f['cols'][col] : col})
            else:
                dataset[col] = ""
        datasets.append(dataset)

    return pd.concat(datasets).to_dict()


def get_keywords(dataset: dict) -> dict:

    x, y = dataset['body'], dataset['is_phishing']
    
    x, x_test, y, y_test = train_test_split(
            x, y, test_size=0.2, random_state=10, stratify=y
    )
    # the actual ML process
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    x_vec = vectorizer.fit_transform(x)
    model = LogisticRegression(max_iter=1000, n_jobs=-1)
    model.fit(x_vec, y)

    y_pred = model.predict(vectorizer.transform(x_test))

    # interpret the model's coeffs
    feature_names = vectorizer.get_feature_names_out()
    coeffs = np.argsort(model.coef_[0])
   
    # output as dict
    wordlist_data = dict()
    for i in coeffs:
        wordlist_data[feature_names[i]] = model.coef_[0][i]

    return wordlist_data
