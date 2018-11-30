import os
import datetime
import sys
import schedule
import time

project_dir1 = os.path.realpath('')
os.chdir(project_dir1+'/Web_Crawler')

def auto_crawler(keyword_1):
    from _master import auto_crawler
    auto_crawler(keyword_1)

def kw_fb_updater(keyword, kw_number):
    from update_fb_comments import facebook_comments_updater
    from update_fb_posts import facebook_posts_updater
    from facebook_search_results import facebook_page_search
    import facebook_access_token as atkn

    if kw_number == 1:
        access_token = atkn.access_token_kw1()
    if kw_number == 2:
        access_token = atkn.access_token_kw2()
    if kw_number == 3:
        access_token = atkn.access_token_kw3()

    print('Updating Facebook. Keyword: %s, %s' % (keyword,datetime.datetime.now()))
    facebook_page_search_results = facebook_page_search(keyword, access_token)
    pages_remaining = len(facebook_page_search_results)
    print('Number pages found for keyword search \"%s\":%s' % (keyword, pages_remaining ))

    for page in facebook_page_search_results:
        facebook_posts_updater(page, access_token, keyword)
        pages_remaining= pages_remaining-1
        print('%s pages remaining to process' % pages_remaining)

    facebook_comments_updater(keyword, access_token)


def kw_instagram_updater(keyword, kw_number):
    from update_insta_hashtags import update_instagram_hashtags_gui
    print('Updating Instagram. Keyword: %s, %s' % (keyword,datetime.datetime.now()))
    update_instagram_hashtags_gui(keyword, kw_number)

def instagram_img_downloader(keyword):
    from instagram_image_downloader import ig_img_downloader
    print('Crawling Instagram Images. Keyword: %s, %s' % (keyword,datetime.datetime.now()))
    ig_img_downloader(keyword)
    print('Done! %s' % datetime.datetime.now())


def kw_twitter_updater(keyword, kw_number):
    from twitter_tweets import update_tweets_gui
    print('Updating Twitter. Keyword: %s, %s' % (keyword,datetime.datetime.now()))
    update_tweets_gui(keyword, kw_number)



############################################################################
project_dir = os.path.realpath('../')
smc = '/Web_Crawler'
gui = '/gui/FlaskApp'
os.chdir(project_dir+gui)
#values for keywords set in /support
kw_settings=open('support/keywords_config', 'r')
kws=kw_settings.readlines()
keyword_1=kws[0].strip()
keyword_2=kws[1].strip()
keyword_3=kws[2].strip()

print('Keywords currently configured:\nkw1: %s \nkw2: %s \nkw3: %s' % (keyword_1,keyword_2,keyword_3) )

kw_settings.close()
os.chdir(project_dir+smc)
############################################################################

def bundle_twitter_updater():
    kw_twitter_updater(keyword_1, 1)
    kw_twitter_updater(keyword_2, 2)
    kw_twitter_updater(keyword_3, 3)

def bundle_instagram_updater():
    kw_instagram_updater(keyword_1, 1)
    kw_instagram_updater(keyword_2, 2)
    kw_instagram_updater(keyword_3, 3)

def bundle_facebook_updater():
    kw_fb_updater(keyword_1, 1)
    kw_fb_updater(keyword_2, 2)
    kw_fb_updater(keyword_3, 3)

print('Going to Scheduler: %s' % datetime.datetime.now())
schedule.every(30).minutes.do(bundle_twitter_updater)
schedule.every(60).minutes.do(bundle_instagram_updater)
schedule.every().day.at("1:30").do(bundle_facebook_updater)

while True:
    schedule.run_pending()
    time.sleep(1)
