import os
import datetime
import sys

smc = '/Web_Crawler'
project_dir = os.path.realpath('../../')
sys.path.append(project_dir+smc)

def auto_crawler(keyword_1):
    project_dir = os.path.realpath('../../')
    smc = '/Web_Crawler'
    gui = '/gui/FlaskApp'
    os.chdir(project_dir+smc)
    from _master import auto_crawler
    auto_crawler(keyword_1)
    os.chdir(project_dir+gui)

def kw_fb_updater(keyword, kw_number):
    project_dir = os.path.realpath('../../')
    smc = '/Web_Crawler'
    gui = '/gui/FlaskApp'
    os.chdir(project_dir+smc)
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
    os.chdir(project_dir+gui)


def kw_instagram_updater(keyword, kw_number):
    project_dir = os.path.realpath('../../')
    smc = '/Web_Crawler'
    gui = '/gui/FlaskApp'
    os.chdir(project_dir+smc)

    from update_insta_hashtags import update_instagram_hashtags_gui
    print('Updating Instagram. Keyword: %s, %s' % (keyword,datetime.datetime.now()))
    update_instagram_hashtags_gui(keyword, kw_number)

    os.chdir(project_dir+gui)

def instagram_img_downloader(keyword):
    project_dir = os.path.realpath('../../')
    smc = '/Web_Crawler'
    gui = '/gui/FlaskApp'
    os.chdir(project_dir+smc)

    from instagram_image_downloader import ig_img_downloader
    print('Crawling Instagram Images. Keyword: %s, %s' % (keyword,datetime.datetime.now()))
    ig_img_downloader(keyword)
    print('Done! %s' % datetime.datetime.now())
    os.chdir(project_dir+gui)


def kw_twitter_updater(keyword, kw_number):
    project_dir = os.path.realpath('../../')
    smc = '/Web_Crawler'
    gui = '/gui/FlaskApp'
    os.chdir(project_dir+smc)

    from twitter_tweets import update_tweets_gui
    print('Updating Twitter. Keyword: %s, %s' % (keyword,datetime.datetime.now()))
    update_tweets_gui(keyword, kw_number)

    os.chdir(project_dir+gui)
