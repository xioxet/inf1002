from machine_learning import COMPILED_DATASETS
from nltk.tokenize import word_tokenize 
from data_parsing import ProcessedEmail
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re, ipaddress

def keyword_analysis(email: ProcessedEmail) -> int:
    keywords = COMPILED_DATASETS['keywords']
    message_words = [word.lower() for word in word_tokenize(email.message)]
    total_score = 0
    for word in message_words:
        if word in keywords:
            total_score += keywords[word]
    return total_score
    
## Url Rule based

def url_detection(text): #url detection
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

    for pattern in url_patterns:
        if re.findall(pattern, text):
            url_link = re.findall(pattern,text)
            print(url_link)
            #all urls will be stored in list.
            return url_link
    print('No Url Detected')
    return False

def url_claimed_domain_checker(html_m):
    #Parse HTML
    soup = BeautifulSoup(html_m, "html.parser")
    
    #Loop through all <a> tags
    for link in soup.find_all("a"):
        text = link.get_text(strip=True)
        if url_detection(text) != False:
            href = link.get("href")
            #Extract domain from href
            parsed_url = urlparse(href)
            actual_domain = parsed_url.netloc
            if actual_domain.lower() in text.lower():
                print("Domain matches claimed text")
            else:
                print("Domain may not match claimed text")
        else:
            print('No url Detected!')
            
def url_scheme_checker(url):
    link = urlparse(url)
    #only allow https because unlikely for email user to face ftp,mailto, tel scheme
    allowed_schemes = {"https"} #can change to read from file
    if link.scheme in allowed_schemes:
        print (link.scheme)
    else:
        print('Suspicious scheme')

def urL_ip_checker(text):
    link = urlparse(text)
    try:
        if ipaddress.ip_address(link.hostname):
            print ('Suspicial url, the hostname are ipaddress.')
    except ValueError:
        print('No IP address in the hostname, seems okay!')