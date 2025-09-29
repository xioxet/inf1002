import difflib  # checks for similarity ratio
import idna     # to normalize domain names to ASCII Characters



# trusted_domains should call the whitelist


trusted_domains = ["microsoft.com", "paypal.com", "google.com"] #example



#This function uses Punycode to normalize all foreign characters to ASCII Characters
def normalize_domain(domain):
    try:
        return idna.encode(domain).decode("utf-8")
    except Exception:
        return domain
    
#Checks the similarity score and returns a float between 0.0 and 1.0
#If True, suspicious
#If False, real domain
def is_similar(domain, whitelist, threshold=0.8):
    for legit in whitelist:
        ratio = difflib.SequenceMatcher(None, domain, legit).ratio()
        if ratio >= threshold:
            return True, legit, ratio
    return False, None, None

#Loops through whitelist and flags sus emails
def check_emails(email_list):
    for email in email_list:
        domain = email.split("@")[-1]
        domain = normalize_domain(domain)
        
        flag, legit, score = is_similar(domain, trusted_domains)
        if flag:
            print(f"Domain '{domain}' is similar to '{legit}' (score: {score:.2f})")
        else:
            return




# emails should call the email extracted from email parsing(?)
emails = [
    "support@rnicrosoft.com",
    "timetopay@paypA1.com",
    "admin@google.com",
    "info@secure-check.net"
]   # example

check_emails(emails)