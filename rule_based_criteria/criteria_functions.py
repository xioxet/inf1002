from dataset_generation import COMPILED_DATASETS
from data_parsing import ProcessedEmail
from bs4 import BeautifulSoup
import re, ipaddress, virustotal_python, os
from pprint import pprint
from hashlib import sha256
from base64 import urlsafe_b64encode

from .utils import *
from utils import *

#VirusTotal API Key
virusTotal_API_key = "7d7b6d2eb25c613fecc1b3a5bb5ccd1cdfeecc6312f390a6237c3f66036a4de3"

def sender_domain_checker(email: ProcessedEmail) -> int:
   
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
        score -= 5
        print(f'{domain} is in the whitelist')
    elif domain in blacklist:
        score += 5
        print(f'{domain} is in the blacklist')
    else:
        print(f'{domain} is unknown')
    
    print(f'Risk score: {score}')
    
    return score

def domain_checker(email: ProcessedEmail) -> int:
    domains = deserialize(COMPILED_DATASETS['domains'])
    score = 0
    # add score here ....
    return score


def keyword_analysis(email: ProcessedEmail) -> int:
    keywords = deserialize(COMPILED_DATASETS['keywords']) # deserialization is cached
    message_words = [word.lower() for word in word_tokenize(email.message)]
    total_score = 0
    for word in message_words:
        if word in keywords:
            total_score += keywords[word]
    return total_score


def scan_attachment_url(email: ProcessedEmail):
    dict = {}
    url_obj = get_all_urls(email.message)
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
        

def check_urls(email: ProcessedEmail) -> int:
    all_urls = get_all_urls(email.message)
    score = 0
    for url in all_urls:
        score += urL_ip_checker(url)
    score += url_claimed_domain_checker(email.message)
    return score
    
