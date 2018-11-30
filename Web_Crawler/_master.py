from os.path import dirname, join
import schedule
import time
import datetime

#updater dependencies
from update_fb_comments import facebook_comments_updater
from update_fb_posts import facebook_posts_updater
from update_insta_hashtags import update_instagram_hashtags
from twitter_tweets import update_tweets


#batch crawler dependencies
#Facebook
from facebook_search_results import facebook_page_search
from facebook_posts import facebook_posts_crawler, facebook_posts_header
from facebook_comments import facebook_comments_crawler
from facebook_access_token import access_token
#Twitter
from twitter_tweets import twitter_csvcreatefile_header, get_tweets
#Instagram
from instagram_hashtags import get_instagram_posts


#keyword='cascais' #will later on be changed to be an input
#will be necessary to add more access tokens to facebook_access_token.py

def auto_crawler(keyword):
    #Twitter
    try:
        df= open(join(dirname(__file__), '_data/%s_tweets.csv' % keyword), 'r')
        df.close()
    except:
        print('Data relating to %s doesn\'t exist, fetching base files (ETA will highly depend on Facebook activity)' % keyword )
        print('Fetching Twitter data')
        twitter_csvcreatefile_header(keyword)
        get_tweets(keyword)
    
    #Instagram
    try:
        df= open(join(dirname(__file__), '_data/%s_instagram_posts.csv' % keyword), 'r')
        df.close()
    except:
        print('Fetching Instagram data')
        get_instagram_posts(keyword)
    
 
    #Facebook
    try:
        df= open(join(dirname(__file__), '_data/%s_facebook_statuses.csv' % keyword), 'r')
        df= open(join(dirname(__file__), '_data/%s_facebook_comments.csv' % keyword), 'r')
        df.close()
    except:
        print('Fetching Facebook data')
        facebook_posts_header(keyword)
        facebook_page_search_results = facebook_page_search(keyword, access_token())
        pages_remaining = len(facebook_page_search_results)
        print('Number pages found for keyword search \"%s\":%s' % (keyword, pages_remaining ))
    
        for page in facebook_page_search_results:
            facebook_posts_crawler(page, access_token(), keyword)
            pages_remaining= pages_remaining-1
            print('%s pages remaining to process' % pages_remaining)
    
        facebook_comments_crawler(keyword, access_token())
   
    
    
    def facebook_updater():
        print('Updating Facebook. Keyword: %s, %s' % (keyword,datetime.datetime.now()))
        facebook_page_search_results = facebook_page_search(keyword, access_token())
        pages_remaining = len(facebook_page_search_results)
        print('Number pages found for keyword search \"%s\":%s' % (keyword, pages_remaining ))
    
        for page in facebook_page_search_results:
            facebook_posts_updater(page, access_token(), keyword)
            pages_remaining= pages_remaining-1
            print('%s pages remaining to process' % pages_remaining)
    
        facebook_comments_updater(keyword, access_token())
    
    def instagram_updater():
        print('Updating Instagram. Keyword: %s, %s' % (keyword,datetime.datetime.now()))
        update_instagram_hashtags(keyword)
    
    def twitter_updater():
        print('Updating Twitter. Keyword: %s, %s' % (keyword,datetime.datetime.now()))
        update_tweets(keyword)
    
    print('Going to Scheduler: %s' % datetime.datetime.now())
    #base files exist, update data
    #Twitter should be updated every 15/20 mins, eventually every 10/15 mins (with two keys)
    schedule.every(25).minutes.do(twitter_updater)
    #Instagram should be updated every hour, eventually every 30 mins
    schedule.every(60).minutes.do(instagram_updater)
    #Facebook should be updated daily
    schedule.every().day.at("1:30").do(facebook_updater)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
