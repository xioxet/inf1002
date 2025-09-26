import pathlib
import csv, sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import numpy as np
import pickle as pkl

from data_parsing import ProcessedEmail

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

csv.field_size_limit(sys.maxsize) # some of these columns are big.

def normalize_email_datasets(email_csv_files: list) -> list:
    emails = []
    for f in email_csv_files:
        file = pathlib.Path(__file__).parent / 'datasets' / 'emails' / f['filename']
        cols = f['cols']
        with open(file, newline='', encoding='utf-8', errors='ignore') as csvfile:
            rows = csv.DictReader(csvfile)
            for row in rows:
                # initialize null values + rename columns
                for col in cols:
                    if cols[col] is None:
                        row[col] = None
                    else:
                        row[col] = row[cols[col]]
                # i would love to just directly serialize the ProcessedEmail classes but we just cannot have nice things.
                emails.append({
                    'sender': row['sender'],
                    'message': row['message'],
                    'attachments': row['attachments'],
                    'is_phishing': row['is_phishing']
                })
    return emails


def normalize_domain_datasets(domain_files: list) -> dict:

    domain_dataset = {}

    for f in domain_files:
        file = pathlib.Path(__file__).parent / 'datasets' / 'domains' / f['filename']
        dataset = open(file, encoding='utf-8', errors='ignore').read().split('\n')
        for domain in dataset:
            domain_dataset[domain] = f['is_phishing']

    return domain_dataset


def get_keywords(dataset: list) -> dict:

    cols = [(email['message'], email['is_phishing']) for email in dataset]
    x, y = zip(*cols)
    x, x_test, y, y_test = train_test_split(
            x, y, test_size=0.2, random_state=10, stratify=y
    )
    # the actual ML process
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    x_vec = vectorizer.fit_transform(x)
    model = LogisticRegression(max_iter=1000, n_jobs=1)
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

