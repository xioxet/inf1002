from data_parsing import ProcessedEmail
from . import criteria_functions

class Report:
    def __init__(self, email: ProcessedEmail):
        self.email = email
        self.scores = dict()

        self.criteria = [
            {
                'name': 'keyword-analysis',
                'function': criteria_functions.keyword_analysis,
                }
            ,{
                'name': 'virusTotal',
                'function': criteria_functions.virusTotal, 
            }
        ]

    def classify(self):
        for criterium in self.criteria:
            self.scores[criterium['name']] = criterium['function'](self.email)
        return self.scores







