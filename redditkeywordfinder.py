import praw
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def reddit_keyword_search(subreddits, keywords, time_filter='week', limit=100):
    # Initialize Reddit API client (you'll need to fill in your own credentials)
    reddit = praw.Reddit(client_id='YOUR_CLIENT_ID',
                         client_secret='YOUR_CLIENT_SECRET',
                         user_agent='YOUR_USER_AGENT')
    
    results = []
    
    for subreddit in subreddits:
        subreddit = reddit.subreddit(subreddit)
        
        # Search submissions test
        for submission in subreddit.search(query=' OR '.join(keywords), sort='new', time_filter=time_filter, limit=limit):
            if any(keyword.lower() in submission.title.lower() or keyword.lower() in submission.selftext.lower() for keyword in keywords):
                matched_keyword = next(keyword for keyword in keywords if keyword.lower() in submission.title.lower() or keyword.lower() in submission.selftext.lower())
                results.append({
                    'community': subreddit.display_name,
                    'targeted_keyword': matched_keyword,
                    'post_link': f'https://www.reddit.com{submission.permalink}'
                })
        
        # Search comments
        for comment in subreddit.comments(limit=limit):
            if any(keyword.lower() in comment.body.lower() for keyword in keywords):
                matched_keyword = next(keyword for keyword in keywords if keyword.lower() in comment.body.lower())
                results.append({
                    'community': subreddit.display_name,
                    'targeted_keyword': matched_keyword,
                    'post_link': f'https://www.reddit.com{comment.permalink}'
                })
    
    return results

def write_to_google_sheets(results):
    # Set up credentials for Google Sheets API test
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/credentials.json', scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet (you'll need to share your sheet with the email in your credentials) test
    sheet = client.open('Reddit Keyword Results').sheet1

    # Clear existing data (optional) test
    sheet.clear()

    # Write headers test
    headers = ['Community', 'Targeted Keyword', 'Post Link']
    sheet.append_row(headers)

    # Write results test
    for result in results:
        sheet.append_row([result['community'], result['targeted_keyword'], result['post_link']])

# Example usage
subreddits = ['AskReddit', 'personalfinance', 'Frugal']
keywords = ['budget', 'saving money', 'financial advice']

results = reddit_keyword_search(subreddits, keywords)
write_to_google_sheets(results)

print(f"Results have been written to Google Sheets. Total results: {len(results)}")


#Wow dude, why are you spying on me behaviour?