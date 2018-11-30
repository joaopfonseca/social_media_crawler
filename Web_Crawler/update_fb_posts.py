from urllib import request
import json
import datetime
import csv
import time
import pandas as pd

def facebook_posts_updater(page_id, access_token, keyword):
    def request_until_succeed(url):
        req = request.Request(url)
        success = False
        number_of_attempts = 0
        while success is False:
            try:
                response = request.urlopen(req)
                if response.getcode() == 200:
                    success = True
                return response.read()
            except Exception as e:
                print (e)
                number_of_attempts=number_of_attempts+1
                time.sleep(5)
                #print ("Error for URL %s: %s" % (url, datetime.datetime.now()))
                if number_of_attempts > 4:
                    break


    def getFacebookPageFeedData(page_id, access_token, num_statuses):

        # construct the URL string
        base = "https://graph.facebook.com"
        node = "/" + page_id + "/feed"
        parameters = "/?fields=message,link,created_time,type,name,id,likes.limit(1).summary(true),comments.limit(1).summary(true),shares&limit=%s&access_token=%s" % (num_statuses, access_token) # changed
        url = base + node + parameters

        # retrieve data
        data = json.loads(request_until_succeed(url))

        return data

    def processFacebookPageFeedStatus(status):
        # Additionally, some items may not always exist,
        # so must check for existence first

        status_id = status['id']
        status_message = '' if 'message' not in status.keys() else status['message']
        link_name = '' if 'name' not in status.keys() else status['name']
        status_type = status['type']
        status_link = '' if 'link' not in status.keys() else status['link']


        # Time needs special care since a) it's in UTC and
        # b) it's not easy to use in statistical programs.

        status_published = datetime.datetime.strptime(status['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
        #status_published = status_published + datetime.timedelta(hours=-5) # EST
        status_published = status_published.strftime('%Y-%m-%d %H:%M:%S') # best time format for spreadsheet programs

        # Nested items require chaining dictionary keys.

        num_likes = 0 if 'likes' not in status.keys() else status['likes']['summary']['total_count']
        num_comments = 0 if 'comments' not in status.keys() else status['comments']['summary']['total_count']
        num_shares = 0 if 'shares' not in status.keys() else status['shares']['count']


        comments_data = '' if 'comments' not in status.keys() else status['comments']['data']
        comments_cancomment = '' if 'comments' not in status.keys() else status['comments']['summary']['can_comment']
        comments_order = '' if 'comments' not in status.keys() else status['comments']['summary']['order']

        likes_paging = '' if 'paging' not in status['likes'].keys() or 'likes' not in status.keys() else status['likes']['paging']
        likes_can_like = '' if 'likes' not in status.keys() else status['likes']['summary']['can_like']
        likes_has_liked = '' if 'likes' not in status.keys() else status['likes']['summary']['has_liked']

        # return a tuple of all processed data
        return (status_id, status_message, link_name, status_type, status_link,
               status_published, num_likes, num_comments, num_shares,
               comments_data, comments_cancomment, comments_order,likes_paging,
               likes_can_like,likes_has_liked, datetime.datetime.now())

    def updateFacebookPageFeedStatus(page_id, access_token):
        with open('_data/%s_facebook_statuses.csv' % keyword, 'a') as file:
            w = csv.writer(file)
            has_next_page = True
            num_processed = 0   # keep a count on how many we've processed
            scrape_starttime = datetime.datetime.now()
            print( "Updating %s Facebook Page (last 30 days): %s" % (page_id, scrape_starttime) )
            try:
                statuses = getFacebookPageFeedData(page_id, access_token, 100)
            except TypeError:
                has_next_page = False
            while has_next_page:
                for status in statuses['data']:
                    w.writerow(processFacebookPageFeedStatus(status))
                    processFacebookPageFeedStatus(status)
                    post_date = datetime.datetime.strptime(status['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
                    days_ago = (datetime.datetime.today() - post_date).days
                    if days_ago > 30:
                        break
                    # output progress occasionally to make sure code is not stalling
                    num_processed += 1
                    if num_processed % 200 == 0:
                        print( "%s Statuses Updated: %s" % (num_processed, datetime.datetime.now()) )
                # if there is no next page, we're done.
                if 'paging' in statuses.keys():
                    try:
                        statuses = json.loads(request_until_succeed(statuses['paging']['next']))
                    except (KeyError,UnboundLocalError, TypeError):
                        break
                else:
                    has_next_page = False
            print( "Done! %s Statuses Updated in %s\n" % (num_processed, datetime.datetime.now() - scrape_starttime) )

    updateFacebookPageFeedStatus(page_id, access_token)

    df = pd.read_csv('_data/%s_facebook_statuses.csv' % keyword)
    df.sort_values(['time_crawled'], ascending=False).drop_duplicates(['status_id'], keep='first').sort_values(['status_published'], ascending=False).to_csv('_data/%s_facebook_statuses.csv' % keyword, index=False)
