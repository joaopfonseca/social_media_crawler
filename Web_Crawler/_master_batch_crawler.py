#Facebook dependencies
from facebook_search_results import facebook_page_search
from facebook_posts import facebook_posts_crawler, facebook_posts_header
from facebook_comments import facebook_comments_crawler
from facebook_access_token import access_token
#Twitter dependency
from twitter_tweets import twitter_csvcreatefile_header, get_tweets
#Instagram dependency
from instagram_hashtags import get_instagram_posts


def master_batch_crawler(keyword):
    #Twitter
    twitter_csvcreatefile_header(keyword)
    get_tweets(keyword)
    
    #Instagram
    get_instagram_posts(keyword)
    
    #Facebook
    facebook_posts_header(keyword)
    facebook_page_search_results = facebook_page_search(keyword, access_token())
    pages_remaining = len(facebook_page_search_results)
    print('Number pages found for keyword search \"%s\":%s' % (keyword, pages_remaining ))
    
    for page in facebook_page_search_results:
        facebook_posts_crawler(page, access_token(), keyword)
        pages_remaining= pages_remaining-1
        print('%s pages remaining to process' % pages_remaining)
        
    facebook_comments_crawler(keyword, access_token())

