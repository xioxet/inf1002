# utility functions
import re, ipaddress, virustotal_python, os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import validators

'''tokenizes messages'''
def word_tokenize(message: str) -> list:
    words = []
    for word in message.split(' '):
        stripped_word = ''.join([i for i in word.lower() if i in 'abcdefghijklmnopqrstuvwxyz'])
        words.append(stripped_word)
    return words


'''returns urls found in message'''
def get_all_urls(message: str) -> list: #url detection
    # Multiple patterns to catch different URL formats
    url_patterns = r'(?:https?://[^\s@]+|www\.[^\s@]+\.com)'
    urls_found = set() # no duplicates...
    for url in re.findall(url_patterns, message):
        urls_found.add(url)
    return list(urls_found)

def url_claimed_domain_checker(message: str) -> int: 
    #Parse HTML, provided if the content type is html
    score = 0
    soup = BeautifulSoup(message, "html.parser")
    #Loop through all <a> tags
    for link in soup.find_all("a"):
        text = link.get_text(strip=True)
        if get_all_urls(text):
            href = link.get("href")
            #Extract domain from href
            parsed_url = urlparse(href)
            actual_domain = parsed_url.netloc
            if actual_domain.lower() not in text.lower():
                #print("Domain matches claimed text")
                score += 5 
    return score

def url_ip_checker(url: str) -> int:
    pattern = r'(\d{1,3}.){3}\d{1,3}' # simple regex to match IPs
    if re.match(pattern, url):
        return 5
    return 0

