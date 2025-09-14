from machine_learning import COMPILED_DATASETS
from nltk.tokenize import word_tokenize 
from data_parsing import ProcessedEmail


def keyword_analysis(email: ProcessedEmail) -> int:
    keywords = COMPILED_DATASETS['keywords']
    message_words = [word.lower() for word in word_tokenize(email.message)]
    total_score = 0
    for word in message_words:
        if word in keywords:
            total_score += keywords[word]
    return total_score
    
