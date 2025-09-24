import whois
from datetime import datetime #imports the datetime class so you can get the current date and calculate the domain’s age.

def get_domain(email): 
    return email.split('@')[1]

def check_domain_age(domain:str):
    try:
        info=whois.whois(domain) #uses WHOIS to get info

        creation_date=info.creation_date #gets the date the domain was created
        if isinstance(creation_date, list):
            creation_date= creation_date[0] 
        if creation_date is None:
            print(f"Could not find the creation date for {domain}")
            return 0, 0 #age and score

        #To calculate the domain age in days
        today=datetime.now() #gets the current date and time
        age_days=(today-creation_date).days

        print(f"{domain} was created on {creation_date}, age:{age_days} days")

        #scoring
        if age_days < 180:  # less than 6 months old
            print("Domain is less than 6 months old.Higher risk.")
            score=-5
        else:
            print("Domain is more than 6 months old. Lower risk.")
            score=5
        
        return age_days, score

    except Exception as e:
        print(f"WHOIS lookup failed for {domain}: {e}")
        return 0,0  #return both age and score
    
    
# Example usage
email = "charmaine@gmail.com"   
domain = get_domain(email)
print(f"Domain: {domain}")
age_days, score = check_domain_age(domain)
print(f"Domain:{domain}, Age:{age_days} days, Risk score: {score}")
