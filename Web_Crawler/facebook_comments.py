import csv
import facebook
import datetime


def facebook_comments_crawler(keyword, access_token):
    #getting posts' id's from the data we already fetched
    list1=[]
    with open('_data/%s_facebook_statuses.csv' % keyword) as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['comments_data'] == []:
                pass
            else:
                list1.append(row['status_id'])

    def graph():
        return facebook.GraphAPI(access_token= access_token, version="2.10")

    print ( 'Processing %s\'s Status\'s comments: %s' % (keyword,datetime.datetime.now()) )

    def get_comments(statusid):
        #get json data:
        try:
            comment1 = graph().get_object(id=statusid, fields='comments')['comments']['data']
            return comment1
        except KeyError:
            return ""

    f = open('_data/%s_facebook_comments.csv' % keyword, 'w')

    with f as csvfile:
        w = csv.writer(csvfile)
        #kep a count on rows processed
        num_processed = 0
        w.writerow(['status_id','comment_id','comment_message','comment_published', 'time_crawled'])
        for status_id in list1:
            try:
                try:
                    comm = get_comments(status_id)
                    for line in comm:
                        num_processed += 1
                        if num_processed % 1000 == 0:
                            print ("%s Comments Processed: %s" % (num_processed, datetime.datetime.now()))
                        w.writerow([status_id,line['id'],line['message'],line['created_time'],datetime.datetime.now()])
                except KeyboardInterrupt:
                    break
            except:
                print('Unsupported get request.')

    print ( 'Done! %s comments processed: %s' % (num_processed, datetime.datetime.now()) )
