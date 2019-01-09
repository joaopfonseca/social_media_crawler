from InstagramAPI import InstagramAPI
import csv
import datetime
import pandas as pd
import os

def update_instagram_hashtags(keyword, ig_creds):
    username = ig_creds['username']
    pwd = ig_creds['pwd']

    directory = 'data/'+keyword
    if not os.path.exists(directory):
        os.makedirs(directory)

    api = InstagramAPI(username, pwd)
    api.login()

    f = open(directory+'/%s_instagram_posts.csv' % keyword, 'a')
    w = csv.writer(f)


    jsono = ['can_viewer_save', 'caption','caption_is_edited','client_cache_key','code',
             'comment_count','comment_likes_enabled','comment_threading_enabled','device_timestamp',
             'filter_type','has_audio','has_liked','has_more_comments','id','image_versions2',
             'is_dash_eligible','like_count','max_num_visible_preview_comments','media_type',
             'number_of_qualities','organic_tracking_token','original_height','original_width',
             'photo_of_you','pk','taken_at','user','video_dash_manifest','video_duration',
             'video_versions','view_count','lat','lng','location']

    fields_with_subfields = [
                            'caption',
                            'image_versions2',
                            'user',
                            'location']

    subfields = {'caption':['bit_flags','content_type','created_at','created_at_utc',
                            'did_report_as_spam','media_id','pk','status','text',
                            'type','user','user_id'],
                 'image_versions2':['candidates'],
                 'user':['friendship_status','full_name','has_anonymous_profile_picture',
                         'is_favorite','is_private','is_unpublished','pk','profile_pic_url',
                         'username'],
                 'location':['address','city','external_source','facebook_places_id',
                             'lat','lng','name','pk','short_name']
                 }


    def update_tag_feed(word):
        
        directory = 'data/'+keyword
        if not os.path.exists(directory):
            os.makedirs(directory)

        next_max = 100000 #amount of tag pages which are loaded: 1 equals approx. 70/80 posts
        next_max_id = ''
        i=0

        for n in range(next_max):
            #if i > 1000:
            #    print('Done! %s posts processed' % i)
            #    break
            try:
                api.getHashtagFeed(word,next_max_id)
                data = api.LastJson
            except:
                print('HTTP request limit reached.')
                print('Done! %s posts processed' % i)
                break

            try:
                for post in data['items']:
                    data_row = []
                    for field in jsono:
                        if field in post.keys():
                            if field in fields_with_subfields:
                                for subfield in subfields[field]:
                                    try:
                                        data_row.append(post[field][subfield])
                                    except TypeError:
                                        data_row.append('')
                            else:
                                data_row.append(post[field])
                        else:
                            data_row.append('')
                    if field == 'location' and field not in post.keys():
                        data_row.insert(53,'')
                        data_row.insert(53,'')
                        data_row.insert(53,'')
                        data_row.insert(53,'')
                        data_row.insert(53,'')
                        data_row.insert(53,'')
                        data_row.insert(53,'')
                        data_row.insert(53,'')
                    data_row.append(datetime.datetime.now())
                    w.writerow(data_row)


                    i=i+1
                    if i % 500 == 0:
                        print( "%s Statuses Processed: %s" % (i, datetime.datetime.now()) )
                next_max_id = data["next_max_id"]
            except:
                try:
                    next_max_id = data["next_max_id"]
                except:
                    print("error next_max. Tag: ", next_max_id)
                    print('Done! %s posts processed' % i)
                    break

    update_tag_feed(keyword)

    #Sort by date and remove duplicates (most recent to oldest)
    df = pd.read_csv(directory+'/%s_instagram_posts.csv' % keyword)

    df.sort_values(['time_crawled'], ascending=False)\
        .drop_duplicates(['pk'], keep='first')\
        .sort_values(['taken_at'], ascending=False)\
        [df['time_crawled'].notnull()]\
        .to_csv(directory+'/%s_instagram_posts.csv' % keyword, index=False)

