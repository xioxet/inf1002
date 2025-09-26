from . import main

COMPILED_DATASETS = main.initialize_datasets()
# this returns _func handlers_ to the necessary datasets

#load CSV file into DataFrame
#df = pd.read_csv('CEAS_08.csv')
#
##Function to extract URLs from body
#def extract_urls(text):
#    if pd.isna(text):
#        return''
#    urls = re.findall(r'https?://\S+|www\S+', text)
#    return ', '.join(urls) if urls else ''
#
#apply function to the body column
#df['extracted_urls'] = df['body'].apply(extract_urls)
#
##categorize labels of phishing or non-phishing email
#df['category'] = df['label'].map({1:"phishing", 0:"not phishing"})
#
#
#Extract relevant columns
#extracted_df = df[['sender', 'subject', 'body', 'extracted_urls', 'category']]
#
#Save to new CSV file
#extracted_df.to_csv('extracted_emails.csv', index=False)

