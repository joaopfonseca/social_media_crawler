from InstagramAPI import InstagramAPI
import csv
import datetime
from instagram_access import ig_creds


#crawls posts by hashtag search
def get_instagram_posts(keyword):
    username = ig_creds(1)['username']
    pwd = ig_creds(1)['pwd']


    api = InstagramAPI(username, pwd)
    api.login()

    f = open('_data/%s_instagram_posts.csv' % keyword, 'w')
    w = csv.writer(f)

    w.writerow(['can_viewer_save','caption_bit_flags','caption_content_type','caption_created_at',
                'caption_created_at_utc','caption_did_report_as_spam','caption_media_id','caption_pk',
                'caption_status','caption_text','caption_type','caption_user','caption_user_id',
                'caption_is_edited','client_cache_key','code','comment_count','comment_likes_enabled',
                'comment_threading_enabled','device_timestamp','filter_type','has_audio','has_liked',
                'has_more_comments','id','image_versions2_candidates','is_dash_eligible','like_count',
                'max_num_visible_preview_comments','media_type','number_of_qualities','organic_tracking_token',
                'original_height','original_width','photo_of_you','pk','taken_at','user_friendship_status',
                'user_full_name','user_has_anonymous_profile_picture','user_is_favorite','user_is_private',
                'user_is_unpublished','user_pk','user_profile_pic_url','user_username','video_dash_manifest',
                'video_duration','video_versions','view_count','lat','lng','location_address','location_city',
                'location_external_source','location_facebook_places_id','location_lat','location_lng',
                'location_name','location_pk','location_short_name','time_crawled'])


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


    def get_tag_feed(word):
        next_max = 100000 #amount of tag pages which are loaded: 1 equals approx. 70/80 posts
        next_max_id = ''
        i=0
        for n in range(next_max):
            api.getHashtagFeed(word,next_max_id)
            data = api.LastJson
            try:
                for post in data['items']:
                    data_row = []
                    for field in jsono:
                        if field in post.keys():
                            if field in fields_with_subfields:
                                for subfield in subfields[field]:
                                    try:
                                        #print("'"+field+">"+subfield+"'")
                                        data_row.append(post[field][subfield])
                                    except TypeError:
                                        data_row.append('')
                            else:
                                #print("'"+field+"'")
                                data_row.append(post[field])
                        else:
                            #print("'"+field+"'")
                            data_row.append('')
                    #print("'time_crawled'")
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
                    #print("error next_max. Tag: ", next_max_id)
                    print('Done! %s posts processed' % i)
                    break

    get_tag_feed(keyword)
