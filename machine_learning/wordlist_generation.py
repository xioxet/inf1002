import pandas as pd
import pathlib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import numpy as np
import pickle as pkl

'''helper func to serialize extracted wordlists to disk w/ pickle'''
def pkl_serialize(data: dict, filename: str):
    with open(pathlib.Path(__file__).parent / 'wordlists' / filename, 'rb') as f:
        pkl.dump(data, f)

''' uses numerical regrssion to evaluate weightage of certain keywords as classifiers for phishing/nonphishing'''
''' todo: implement naive bayesian by hand? seems more interesting...'''
def get_keywords(pathname: str) -> dict:
    dataset = pd.read_csv(pathlib.Path(__file__).parent / 'datasets' / pathname)
    x, y = dataset['body'], dataset['label']
    
    x, x_test, y, y_test = train_test_split(
            x, y, test_size=0.2, random_state=10, stratify=y
    )
    # the actual ML process
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    x_vec = vectorizer.fit_transform(x)
    model = LogisticRegression(max_iter=1000, n_jobs=-1)
    model.fit(x_vec, y)

    y_pred = model.predict(vectorizer.transform(x_test))
    print(classification_report(y_test, y_pred))

    # interpret the model's coeffs
    feature_names = vectorizer.get_feature_names_out()
    coeffs = np.argsort(model.coef_[0])
   
    # output as dict
    wordlist_data = dict()
    for i in coeffs:
        wordlist_data[feature_names[i]] = model.coef_[0][i]

    return wordlist_data
