from machine_learning import COMPILED_DATASETS
from nltk.tokenize import word_tokenize 
from data_parsing import ProcessedEmail
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re, ipaddress, virustotal_python, os
from pprint import pprint
from hashlib import sha256

#VirusTotal API Key
virusTotal_API_key = "7d7b6d2eb25c613fecc1b3a5bb5ccd1cdfeecc6312f390a6237c3f66036a4de3"

def sender_domain_checker(email: ProcessedEmail):
   
    #clean_email = email_content.split()[0] #this takes the first world from the str (the real email, ignores any extra word) not sure if still needed
    #print(f"Clean email (without any extra words): {clean_email}"), not sure if still needed

    #blacklist
    blacklist = open((r'C:\Users\Charm\inf1002\email_validation\blacklist.txt')).read().split(" ")

    #whitelist
    whitelist = open((r'C:\Users\Charm\inf1002\email_validation\whitelistf1.txt')).read().split(" ")

    domain = email.sender.split("@")[1]
    
    print(f"Extracted domain: {domain}") #hdb.com <- "jeremy@hdb.com"

    score = 0 

    if domain in whitelist:
        score += 5
        print(f'{domain} is in the whitelist')
    elif domain in blacklist:
        score -= 5
        print(f'{domain} is in the blacklist')
    else:
        print(f'{domain} is unknown')
    
    print(f'Risk score: {score}')
    
    return score



def add(a: int, b: int) -> int:
    return a+b

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


def virusTotal(email: ProcessedEmail):
    #file_path = "./Attachments/attachment.pdf"
    #files = {"file": (os.path.basename(file_path), open(os.path.abspath(file_path), "rb"))}
    dict = {}
    for attachment in email.attachments:
        file_bytes  = attachment.getvalue()
        file_name = getattr(attachment, "name", "myfile.bin")
        file_hash = sha256(file_bytes).hexdigest()
        files = {"file": (file_name, file_bytes)}
        print(file_name)
        with virustotal_python.Virustotal(virusTotal_API_key) as vtotal:
            #will upload into the virustotal, if the file have never been uploaded before
            vtotal.request("files", files=files, method="POST")
            #if the file been uploaded before, will instant get the report, else will be error
            resp = vtotal.request(f"files/{file_hash}").data 
            attribute_totalvotes = resp["attributes"]["total_votes"]
            #more info about the attributes: https://docs.virustotal.com/reference/private-files-api#:~:text=You%20can%20find%20information%20about%20the%20file%27s%20attributes%20in%20here.%20In%20this%20case%20the%20SHA256%20of%20the%20file%20is%206b4bb405d3deea7a63e3ed02dd62a59c69b9458c15a901f3607429325b228ae8%3A 
            dict[file_name] = attribute_totalvotes
    return dict
        

