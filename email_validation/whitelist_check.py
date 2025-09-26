def get_domain(email): #func to get domain from email
    return email.split('@')[1]

def check_risk(email_content, whitelist, blacklist):
    print(f'\nProcessing email:{email_content}') #/n adds a new line before printing

    clean_email = email_content.split()[0] #this takes the first world from the str (the real email, ignores any extra word)
    print(f"Clean email (without any extra words): {clean_email}")

    domain = get_domain(clean_email)
    print(f"Extracted domain: {domain}")

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
    


blacklist = open((r'C:\Users\Charm\inf1002\email_validation\blacklist.txt')).read().split(" ")


whitelist = open((r'C:\Users\Charm\inf1002\email_validation\whitelistf1.txt')).read().split(" ")
