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
    average_dict = {}
    for criterium in Report(None).criteria:
        average_dict[criterium['name']] = []
    
    averages = [{k: [] for k in average_dict} for i in range(2)]
    
    print('now processing all emails to generate averages. this may take a while!')
    for email in tqdm(emails):
        email = type('ProcessedEmail', (object,), email) # python magic
        score_classification = Report(email).classify()
        
        for key, value in score_classification.items():
            averages[email.is_phishing][key] += [value]

    for avg in averages:
        for key in avg:
            avg[key] = sum(avg[key]) / len(avg[key])
        print(avg)


