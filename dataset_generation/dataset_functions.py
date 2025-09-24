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

functionally this is just going to be a list of dicts that we can happy happy join together

some lack the information that we're actually looking for
but this is Ok because this is just for training purposes

this is written with the future in mind: if we need more datasets, we just add it to this list!
'''
def normalize_email_datasets(email_csv_files: list) -> list:
    
    datasets = []
    
    for f in email_csv_files:
        file = pathlib.Path(__file__).parent / 'datasets' / 'emails' / f['filename']
        # csv is easier to deal with
        dataset = pd.read_csv(pathlib.Path(__file__).parent / 'datasets' / 'emails' / f['filename'])
        
        new_df = pd.DataFrame(columns = f['cols'].keys())
        for col in f['cols']:
            original_col = f['cols'][col]
            if not original_col:
                new_df[col] = ""
            elif col == 'is_phishing':
                new_df[col] = dataset[original_col].astype(bool)
            else:
                new_df[col] = dataset[original_col].astype(str)


        datasets.append(new_df)

    return pd.concat(datasets).to_dict(orient="records")


def normalize_domain_datasets(domain_files: list) -> dict:

    domain_dataset = {}

    for f in domain_files:
        file = pathlib.Path(__file__).parent / 'datasets' / 'domains' / f['filename']
        dataset = open(file, encoding='utf-8').read().split('\n')
        for domain in dataset:
            domain_dataset[domain] = f['is_phishing']

    return domain_dataset


def get_keywords(dataset: list) -> dict:
    cols = [(email['body'], email['is_phishing']) for email in dataset]
    x, y = zip(*cols)
    for i in x:
        if type(i) != str:
            print(i)
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
