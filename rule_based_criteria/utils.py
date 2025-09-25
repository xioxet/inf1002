# utility functions
import re, ipaddress, virustotal_python, os
from bs4 import BeautifulSoup
from urllib.parse import urlparse

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
    url_patterns = [
        # 1) Schemed URLs (http/https/ftp) incl. auth, IPv4/IPv6, localhost, port, path
        r'(?:https?|ftp)://(?:[^\s:@/]+(?::[^\s:@/]*)?@)?(?:(?:[a-z0-9-]+\.)+(?:[a-z]{2,63}|xn--[a-z0-9-]+)|localhost|\d{1,3}(?:\.\d{1,3}){3}|\[(?:[0-9a-f:.]+)\])(?::\d{2,5})?(?:/[^\s<>()\[\]{}"\']*)?',
        # 2) www.* without scheme
        r'www\.(?:[a-z0-9-]+\.)+(?:[a-z]{2,63}|xn--[a-z0-9-]+)(?::\d{2,5})?(?:/[^\s<>()\[\]{}"\']*)?',
        # 3) bare domain (no scheme/www), optional port+path; avoid emails & scheme/www overlaps
        r'(?<!@)(?<!://)(?<!www\.)(?:[a-z0-9-]+\.)+(?:[a-z]{2,63}|xn--[a-z0-9-]+)(?::\d{2,5})?(?:/[^\s<>()\[\]{}"\']*)?',
        # 4) scheme without // (e.g., https:example.com)
        r'(?:https?|ftp):(?!//)[^\s<>()\[\]{}"\']+'
    ]
    

    urls_found = []
    for pattern in url_patterns:
        for url in re.findall(pattern, message):
            urls_found.append(url)

    return urls_found

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

def url_scheme_checker(url: str) -> int:
    link = urlparse(url)
    score = 0
    #only allow https because unlikely for email user to face ftp,mailto, tel scheme
    allowed_schemes = {"https"} #can change to read from file
    if link.scheme not in allowed_schemes:
        score += 5
    return score

def urL_ip_checker(url: str) -> int:
    pattern = r'(\d{1,3}.){3}\d{1,3}' # simple regex to match urls
    if re.match(pattern, url):
        return 5
    return 0

