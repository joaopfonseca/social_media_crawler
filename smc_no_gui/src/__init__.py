from os.path import dirname, join

import sys, os
sys.path.append(os.path.dirname(__file__))


import schedule
import time
import datetime

# API access credentials
from creds import instagram_creds, twitter_creds

#updater dependencies
from update_insta_hashtags import update_instagram_hashtags
from twitter_tweets import update_tweets


#batch crawler dependencies
#Twitter
from twitter_tweets import twitter_csvcreatefile_header, get_tweets
#Instagram
from instagram_hashtags import get_instagram_posts
from instagram_image_downloader import ig_img_downloader


#keyword='cascais' #will later on be changed to be an input
#will be necessary to add more access tokens to facebook_access_token.py

def auto_crawler(keyword, kw_number):
    """
    Checks for existence of keyword-related data. Updates periodically if data exists. Generates files with inital data if none is found.
    Params:
    - keyword: keyword to search for. Must not contain spaces or special case letters.
    - kw_number: credentials number to which you wish to associate the keyword and crawling process to.
    """

    directory = 'data/'+keyword
    if not os.path.exists(directory):
        os.makedirs(directory)


    # establishing access credentials
    ig_creds = instagram_creds(kw_number)
    t_creds  = twitter_creds(kw_number)
    
    
    def instagram_updater():
        print('Updating Instagram. Keyword: %s, %s' % (keyword,datetime.datetime.now()))
        update_instagram_hashtags(keyword, ig_creds)
    
    def instagram_img_updater():
        print('Downloading Instagram pictures from posts crawled in the last 24h. Keyword: %s, %s' % (keyword,datetime.datetime.now()))
        ig_img_downloader(keyword)
        
    def twitter_updater():
        print('Updating Twitter. Keyword: %s, %s' % (keyword,datetime.datetime.now()))
        update_tweets(keyword, t_creds)
    

    #Twitter
    try:
        f = open(directory+'/%s_tweets.csv' % keyword, 'r')
        f.close()
        twitter_updater()
    except FileNotFoundError as e:
        print(e)
        print('Twitter Data relating to %s not found, creating csv files and crawling first batch' % keyword )
        twitter_csvcreatefile_header(keyword)
        get_tweets(keyword, t_creds)

    #Instagram
    try:
        f = open(directory+'/%s_instagram_posts.csv' % keyword, 'r')
        f.close()
        instagram_updater()
        instagram_img_updater()
    except FileNotFoundError as e:
        print(e)
        print('Instagram data relating to %s not found, creating csv files and crawling first batch' % keyword )
        get_instagram_posts(keyword, ig_creds)
        print('Downloading Instagram pictures from posts crawled in the last 24h. Keyword: %s, %s' % (keyword,datetime.datetime.now()))
        ig_img_downloader(keyword)

    print('Going to Scheduler: %s' % datetime.datetime.now())
    #base files exist, update data
    #Twitter should be updated every 15/20 mins, eventually every 10/15 mins
    schedule.every(25).minutes.do(twitter_updater)
    #Instagram should be updated every hour, eventually every 30 mins
    schedule.every(25).minutes.do(instagram_updater)
    schedule.every(120).minutes.do(instagram_img_updater)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
