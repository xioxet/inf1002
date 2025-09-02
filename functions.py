#All the functions 
import re


def has_url(text):
    # Multiple patterns to catch different URL formats
    url_patterns = [
        r'https?://[^\s]+',  # Standard http/https URLs
        r'https?:[^\s]+',    # Malformed URLs like https:example.com
        r'\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?',  # Domain names like example.com
        r'www\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?'  # www.example.com
    ]
    
    for pattern in url_patterns:
        if re.search(pattern, text):
            return print('Have URL')
    return print('No URL')