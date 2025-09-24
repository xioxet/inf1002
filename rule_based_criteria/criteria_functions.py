from dataset_generation import COMPILED_DATASETS
from data_parsing import ProcessedEmail
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re, ipaddress, virustotal_python, os
from pprint import pprint
from hashlib import sha256
from base64 import urlsafe_b64encode

#VirusTotal API Key
virusTotal_API_key = ""

def sender_domain_checker(email: ProcessedEmail):
   
    #clean_email = email_content.split()[0] #this takes the first world from the str (the real email, ignores any extra word) not sure if still needed
    #print(f"Clean email (without any extra words): {clean_email}"), not sure if still needed

    #blacklist
    blacklist = open((r'\blacklist.txt')).read().split(" ")

    #whitelist
    whitelist = open((r'\whitelistf1.txt')).read().split(" ")

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

def keyword_analysis(email: ProcessedEmail) -> int:
    keywords = COMPILED_DATASETS['keywords']
    message_words = [word.lower() for word in email.message]
    total_score = 0
    for word in message_words:
        if word in keywords:
            total_score += keywords[word]
    return total_score

## Url Rule based

def url_detection(message): #url detection
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
        if re.findall(pattern, message):
            url_link = re.findall(pattern, message)
            #all urls will be stored in list.
            return url_link
    return False

def url_claimed_domain_checker(message): 
    #Parse HTML, provided if the content type is html
    score = 0
    soup = BeautifulSoup(message, "html.parser")
    #Loop through all <a> tags
    for link in soup.find_all("a"):
        text = link.get_text(strip=True)
        if url_detection(text) != False:
            href = link.get("href")
            #Extract domain from href
            parsed_url = urlparse(href)
            actual_domain = parsed_url.netloc
            if actual_domain.lower() not in text.lower():
                #print("Domain matches claimed text")
                score += 5 
    return score
            
def url_scheme_checker(url):
    link = urlparse(url)
    score = 0
    #only allow https because unlikely for email user to face ftp,mailto, tel scheme
    allowed_schemes = {"https"} #can change to read from file
    if link.scheme not in allowed_schemes:
        score += 5
    return score

def urL_ip_checker(text):
    link = urlparse(text)
    score = 0
    try:
        if ipaddress.ip_address(link.hostname):
            score += 5 #if there's ip address within the url
            return score
    except ValueError:
        return score
 

def virusTotal(email: ProcessedEmail):
    dict = {}
    url_obj = url_detection(email.message)
    if email.attachments:
        for attachment in email.attachments:
            file_bytes  = attachment.getvalue()
            file_name = getattr(attachment, "name", "myfile.bin")
            file_hash = sha256(file_bytes).hexdigest()
            files = {"file": (file_name, file_bytes)}
            with virustotal_python.Virustotal(virusTotal_API_key) as vtotal:
                #will upload into the virustotal, if the file have never been uploaded before
                vtotal.request("files", files=files, method="POST")
                #if the file been uploaded before, will instant get the report, else will be error
                resp = vtotal.request(f"files/{file_hash}").data 
                dict[file_name]= resp["attributes"]["total_votes"]
                #more info about the attributes: https://docs.virustotal.com/reference/private-files-api#:~:text=You%20can%20find%20information%20about%20the%20file%27s%20attributes%20in%20here.%20In%20this%20case%20the%20SHA256%20of%20the%20file%20is%206b4bb405d3deea7a63e3ed02dd62a59c69b9458c15a901f3607429325b228ae8%3A 
    elif url_obj:
       for url_link in url_obj:
           with virustotal_python.Virustotal(virusTotal_API_key) as vtotal:
            try:
                resp = vtotal.request("urls", data={"url": url_link}, method="POST")
                # Safe encode URL in base64 format
                # https://developers.virustotal.com/reference/url
                url_id = urlsafe_b64encode(url_link.encode()).decode().strip("=")
                report = vtotal.request(f"urls/{url_id}").data
                dict[url_link] = report["attributes"]["total_votes"]
            except virustotal_python.VirustotalError as err:
                print(f"Failed to send URL: {url_link} for analysis and get the report: {err}")
    return dict
        
def Url_Checker_Overall(email: ProcessedEmail):
    status_url_detection = url_detection(email.message)
    score = 0
    if status_url_detection != False:
        for i in status_url_detection:
            score += urL_ip_checker(i)
            score += url_scheme_checker(i)
        score += url_claimed_domain_checker(email.message)
    return score
    
