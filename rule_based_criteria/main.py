from data_parsing import ProcessedEmail
from . import criteria_functions
from dataset_generation import COMPILED_DATASETS
from utils import *
from tqdm import tqdm

class Report:
    def __init__(self, email: ProcessedEmail):
        self.email = email
        self.scores = dict()

        self.criteria = [
            {
                'name': 'keyword-analysis',
                'function': criteria_functions.keyword_analysis,
            },
             
            {
                'name': 'url-detection',
                'function': criteria_functions.check_urls
            }
        ]

    def classify(self) -> dict:
        for criterium in self.criteria:
            self.scores[criterium['name']] = criterium['function'](self.email)
        return self.scores


# ok this is where shit actually happens

def get_average_scores_of_dataset():
    emails = deserialize(COMPILED_DATASETS['emails'])
    ham_avg = {}
    spam_avg = {}
    z = [ham_avg, spam_avg]
    for key in emails[0]:
        ham_avg[key] = []
        spam_avg[key] = []

    print('now processing all emails to generate averages. this may take a while!')
    for email in tqdm(emails):
        email = type('ProcessedEmail', (object,), email) # python magic
        score_classification = Report(email).classify()
        


