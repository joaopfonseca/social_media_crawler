import tweepy
import csv
import datetime
import pandas as pd
import os


def twitter_csvcreatefile_header(keyword):
    
    directory = 'data/'+keyword
    if not os.path.exists(directory):
        os.makedirs(directory)

    f = open(directory+'/%s_tweets.csv' % keyword, 'w')
    with f as file:
        w = csv.writer(file)
        w.writerow(['contributors',
                    'coordinates',
                    'created_at',
                    'entities_hashtags',
                    'entities_symbols',
                    'entities_urls',
                    'entities_user_mentions',
                    'favorite_count',
                    'favorited',
                    'geo',
                    'id',
                    'id_str',
                    'in_reply_to_screen_name',
                    'in_reply_to_status_id',
                    'in_reply_to_status_id_str',
                    'in_reply_to_user_id_iso_language_code',
                    'in_reply_to_user_id_str_result_type',
                    'is_quote_status',
                    'lang',
                    'metadata_iso_language_code',
                    'metadata_result_type',
                    'place',
                    'retweet_count',
                    'retweeted',
                    'retweeted_status_contributors',
                    'retweeted_status_coordinates',
                    'retweeted_status_created_at',
                    'retweeted_status_entities',
                    'retweeted_status_favorite_count',
                    'retweeted_status_favorited',
                    'retweeted_status_geo',
                    'retweeted_status_id',
                    'retweeted_status_id_str',
                    'retweeted_status_in_reply_to_screen_name',
                    'retweeted_status_in_reply_to_status_id',
                    'retweeted_status_in_reply_to_status_id_str',
                    'retweeted_status_in_reply_to_user_id',
                    'retweeted_status_in_reply_to_user_id_str',
                    'retweeted_status_is_quote_status',
                    'retweeted_status_lang',
                    'retweeted_status_metadata',
                    'retweeted_status_place',
                    'retweeted_status_retweet_count',
                    'retweeted_status_retweeted',
                    'retweeted_status_source',
                    'retweeted_status_text',
                    'retweeted_status_truncated',
                    'retweeted_status_user',
                    'source',
                    'text',
                    'truncated',
                    'user_contributors_enabled',
                    'user_created_at',
                    'user_default_profile',
                    'user_default_profile_image',
                    'user_description',
                    'user_favourites_count',
                    'user_follow_request_sent',
                    'user_followers_count',
                    'user_following',
                    'user_friends_count',
                    'user_geo_enabled',
                    'user_has_extended_profile',
                    'user_id',
                    'user_id_str',
                    'user_is_translation_enabled',
                    'user_is_translator',
                    'user_lang',
                    'user_listed_count',
                    'user_location',
                    'user_name',
                    'user_notifications',
                    'user_profile_background_color',
                    'user_profile_background_image_url',
                    'user_profile_background_image_url_https',
                    'user_profile_background_tile',
                    'user_profile_banner_url',
                    'user_profile_image_url',
                    'user_profile_image_url_https',
                    'user_profile_link_color',
                    'user_profile_sidebar_border_color',
                    'user_profile_sidebar_fill_color',
                    'user_profile_text_color',
                    'user_profile_use_background_image',
                    'user_protected',
                    'user_screen_name',
                    'user_statuses_count',
                    'user_time_zone',
                    'user_translator_type',
                    'user_url',
                    'user_utc_offset',
                    'user_verified',
                    'time_crawled'
                    ])





def update_tweets(keyword, twitter_creds):
    def if_empty(json_input):
        if json_input == '':
            return ''
        else:
            return json_input


    def json_check_keys(jsono):
        print(jsono.keys())

    jsono = ['contributors','coordinates','created_at','entities','favorite_count','favorited',
             'geo','id','id_str','in_reply_to_screen_name','in_reply_to_status_id',
             'in_reply_to_status_id_str','in_reply_to_user_id','in_reply_to_user_id_str',
             'is_quote_status','lang','metadata','place','retweet_count','retweeted',
             'retweeted_status','source','text','truncated','user']

    fields_with_subfields = ['entities','in_reply_to_user_id','in_reply_to_user_id_str',
                             'metadata','retweeted_status','user']

    subfields= {'entities':['hashtags','symbols','urls','user_mentions'],
                'in_reply_to_user_id':['iso_language_code'],
                'in_reply_to_user_id_str':['result_type'],
                'metadata':['iso_language_code','result_type'],
                'retweeted_status': ['contributors','coordinates','created_at','entities',
                                     'favorite_count','favorited','geo','id','id_str',
                                     'in_reply_to_screen_name','in_reply_to_status_id',
                                     'in_reply_to_status_id_str','in_reply_to_user_id',
                                     'in_reply_to_user_id_str','is_quote_status','lang',
                                     'metadata','place','retweet_count','retweeted',
                                     'source','text','truncated','user'],
                'user':['contributors_enabled','created_at','default_profile',
                        'default_profile_image','description','favourites_count',
                        'follow_request_sent','followers_count','following','friends_count',
                        'geo_enabled','has_extended_profile','id','id_str',
                        'is_translation_enabled','is_translator','lang','listed_count','location',
                        'name','notifications','profile_background_color',
                        'profile_background_image_url','profile_background_image_url_https',
                        'profile_background_tile','profile_banner_url','profile_image_url',
                        'profile_image_url_https','profile_link_color',
                        'profile_sidebar_border_color','profile_sidebar_fill_color',
                        'profile_text_color','profile_use_background_image','protected',
                        'screen_name','statuses_count','time_zone','translator_type','url',
                        'utc_offset','verified']}

    API_KEY = twitter_creds['API_KEY']
    API_SECRET = twitter_creds['API_SECRET']
    ACCESS_TOKEN = twitter_creds['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = twitter_creds['ACCESS_TOKEN_SECRET']
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api= tweepy.API(auth)

    max_tweets = 2000
    print ( 'Processing %s Tweets containing the term \"%s\": %s' % (max_tweets,keyword,datetime.datetime.now()) )

    try:
        searched_tweets = [status for status in tweepy.Cursor(api.search, q=keyword).items(max_tweets)]

        directory = 'data/'+keyword
        if not os.path.exists(directory):
            os.makedirs(directory)

        f = open(directory+'/%s_tweets.csv' % keyword, 'a')

        with f as file:
            i=0
            w = csv.writer(file)
            for tweet in searched_tweets:
                i=i+1
                data_row=[]
                for field in jsono:
                    if field in tweet._json.keys():
                        if field in fields_with_subfields:
                            for subfield in subfields[field]:
                                try:
                                    data_row.append(tweet._json[field][subfield])
                                except:
                                    data_row.append('')
                        else:
                            if_empty(data_row.append(tweet._json[field]))

                    else:
                        data_row.append('')

                if 'retweeted_status' not in tweet._json.keys():
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                data_row.append(datetime.datetime.now())
                w.writerow(data_row)
        df = pd.read_csv(directory+'/%s_tweets.csv' % keyword)
        df['id'] = df['id'].apply(str)
        df.sort_values(['time_crawled'], ascending=False).drop_duplicates(['id'], keep='first').sort_values(['created_at'], ascending=False).to_csv(directory+'/%s_tweets.csv' % keyword, index=False)
        print('Done! %s Tweets processed: %s' % (i, datetime.datetime.now()))
    except:
        print('Failed to send request: Read timed out.')


def get_tweets(keyword, twitter_creds):
    def if_empty(json_input):
        if json_input == '':
            return ''
        else:
            return json_input


    def json_check_keys(jsono):
        print(jsono.keys())

    jsono = ['contributors','coordinates','created_at','entities','favorite_count','favorited',
             'geo','id','id_str','in_reply_to_screen_name','in_reply_to_status_id',
             'in_reply_to_status_id_str','in_reply_to_user_id','in_reply_to_user_id_str',
             'is_quote_status','lang','metadata','place','retweet_count','retweeted',
             'retweeted_status','source','text','truncated','user']

    fields_with_subfields = ['entities','in_reply_to_user_id','in_reply_to_user_id_str',
                             'metadata','retweeted_status','user']

    subfields= {'entities':['hashtags','symbols','urls','user_mentions'],
                'in_reply_to_user_id':['iso_language_code'],
                'in_reply_to_user_id_str':['result_type'],
                'metadata':['iso_language_code','result_type'],
                'retweeted_status': ['contributors','coordinates','created_at','entities',
                                     'favorite_count','favorited','geo','id','id_str',
                                     'in_reply_to_screen_name','in_reply_to_status_id',
                                     'in_reply_to_status_id_str','in_reply_to_user_id',
                                     'in_reply_to_user_id_str','is_quote_status','lang',
                                     'metadata','place','retweet_count','retweeted',
                                     'source','text','truncated','user'],
                'user':['contributors_enabled','created_at','default_profile',
                        'default_profile_image','description','favourites_count',
                        'follow_request_sent','followers_count','following','friends_count',
                        'geo_enabled','has_extended_profile','id','id_str',
                        'is_translation_enabled','is_translator','lang','listed_count','location',
                        'name','notifications','profile_background_color',
                        'profile_background_image_url','profile_background_image_url_https',
                        'profile_background_tile','profile_banner_url','profile_image_url',
                        'profile_image_url_https','profile_link_color',
                        'profile_sidebar_border_color','profile_sidebar_fill_color',
                        'profile_text_color','profile_use_background_image','protected',
                        'screen_name','statuses_count','time_zone','translator_type','url',
                        'utc_offset','verified']}

    API_KEY = twitter_creds['API_KEY']
    API_SECRET = twitter_creds['API_SECRET']
    ACCESS_TOKEN = twitter_creds['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = twitter_creds['ACCESS_TOKEN_SECRET']
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api= tweepy.API(auth)

    max_tweets = 2000
    print ( 'Processing %s Tweets containing the term \"%s\": %s' % (max_tweets,keyword,datetime.datetime.now()) )

    searched_tweets = [status for status in tweepy.Cursor(api.search, q=keyword).items(max_tweets)]

    directory = 'data/'+keyword
    if not os.path.exists(directory):
        os.makedirs(directory)

    f = open(directory+'/%s_tweets.csv' % keyword, 'a')


    with f as file:
        i=0
        w = csv.writer(file)
        for tweet in searched_tweets:
            i=i+1
            data_row=[]
            for field in jsono:
                if field in tweet._json.keys():
                    if field in fields_with_subfields:
                        for subfield in subfields[field]:
                            try:
                                data_row.append(tweet._json[field][subfield])
                            except:
                                data_row.append('')
                    else:
                        if_empty(data_row.append(tweet._json[field]))

                else:
                    data_row.append('')

            if 'retweeted_status' not in tweet._json.keys():
                data_row.insert(25, '')
                data_row.insert(25, '')
                data_row.insert(25, '')
                data_row.insert(25, '')
                data_row.insert(25, '')
                data_row.insert(25, '')
                data_row.insert(25, '')
                data_row.insert(25, '')
                data_row.insert(25, '')
                data_row.insert(25, '')
                data_row.insert(25, '')
                data_row.insert(25, '')
                data_row.insert(25, '')
                data_row.insert(25, '')
                data_row.insert(25, '')
                data_row.insert(25, '')
                data_row.insert(25, '')
                data_row.insert(25, '')
                data_row.insert(25, '')
                data_row.insert(25, '')
                data_row.insert(25, '')
                data_row.insert(25, '')
                data_row.insert(25, '')
            data_row.append(datetime.datetime.now())
            w.writerow(data_row)
    print('Done! %s Tweets processed: %s' % (i, datetime.datetime.now()))


def update_tweets_gui(keyword, twitter_creds):

    def if_empty(json_input):
        if json_input == '':
            return ''
        else:
            return json_input


    def json_check_keys(jsono):
        print(jsono.keys())

    jsono = ['contributors','coordinates','created_at','entities','favorite_count','favorited',
             'geo','id','id_str','in_reply_to_screen_name','in_reply_to_status_id',
             'in_reply_to_status_id_str','in_reply_to_user_id','in_reply_to_user_id_str',
             'is_quote_status','lang','metadata','place','retweet_count','retweeted',
             'retweeted_status','source','text','truncated','user']

    fields_with_subfields = ['entities','in_reply_to_user_id','in_reply_to_user_id_str',
                             'metadata','retweeted_status','user']

    subfields= {'entities':['hashtags','symbols','urls','user_mentions'],
                'in_reply_to_user_id':['iso_language_code'],
                'in_reply_to_user_id_str':['result_type'],
                'metadata':['iso_language_code','result_type'],
                'retweeted_status': ['contributors','coordinates','created_at','entities',
                                     'favorite_count','favorited','geo','id','id_str',
                                     'in_reply_to_screen_name','in_reply_to_status_id',
                                     'in_reply_to_status_id_str','in_reply_to_user_id',
                                     'in_reply_to_user_id_str','is_quote_status','lang',
                                     'metadata','place','retweet_count','retweeted',
                                     'source','text','truncated','user'],
                'user':['contributors_enabled','created_at','default_profile',
                        'default_profile_image','description','favourites_count',
                        'follow_request_sent','followers_count','following','friends_count',
                        'geo_enabled','has_extended_profile','id','id_str',
                        'is_translation_enabled','is_translator','lang','listed_count','location',
                        'name','notifications','profile_background_color',
                        'profile_background_image_url','profile_background_image_url_https',
                        'profile_background_tile','profile_banner_url','profile_image_url',
                        'profile_image_url_https','profile_link_color',
                        'profile_sidebar_border_color','profile_sidebar_fill_color',
                        'profile_text_color','profile_use_background_image','protected',
                        'screen_name','statuses_count','time_zone','translator_type','url',
                        'utc_offset','verified']}

    API_KEY = twitter_creds['API_KEY']
    API_SECRET = twitter_creds['API_SECRET']
    ACCESS_TOKEN = twitter_creds['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = twitter_creds['ACCESS_TOKEN_SECRET']

    directory = 'data/'+keyword
    if not os.path.exists(directory):
        os.makedirs(directory)


    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api= tweepy.API(auth)

    max_tweets = 2000
    print ( 'Processing %s Tweets containing the term \"%s\": %s' % (max_tweets,keyword,datetime.datetime.now()) )

    try:
        searched_tweets = [status for status in tweepy.Cursor(api.search, q=keyword).items(max_tweets)]

        f = open(directory+'/%s_tweets.csv' % keyword, 'a')

        with f as file:
            i=0
            w = csv.writer(file)
            for tweet in searched_tweets:
                i=i+1
                data_row=[]
                for field in jsono:
                    if field in tweet._json.keys():
                        if field in fields_with_subfields:
                            for subfield in subfields[field]:
                                try:
                                    data_row.append(tweet._json[field][subfield])
                                except:
                                    data_row.append('')
                        else:
                            if_empty(data_row.append(tweet._json[field]))

                    else:
                        data_row.append('')

                if 'retweeted_status' not in tweet._json.keys():
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                    data_row.insert(25, '')
                data_row.append(datetime.datetime.now())
                w.writerow(data_row)
        df = pd.read_csv(directory+'/%s_tweets.csv' % keyword)
        df['id'] = df['id'].apply(str)
        df.sort_values(['time_crawled'], ascending=False).drop_duplicates(['id'], keep='first').sort_values(['created_at'], ascending=False).to_csv(directory+'/%s_tweets.csv' % keyword, index=False)
        print('Done! %s Tweets processed: %s' % (i, datetime.datetime.now()))
    except Exception as e:
        print(e)
