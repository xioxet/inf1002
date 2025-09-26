from data_parsing import ProcessedEmail
from . import criteria_functions
from dataset_generation import COMPILED_DATASETS
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
    emails = COMPILED_DATASETS['emails']
    for email in emails:
        print(email)
        email = type('ProcessedEmail', (object,), email) # python magic
        score_classification = Report(email).classify()
        print(score_classification)


