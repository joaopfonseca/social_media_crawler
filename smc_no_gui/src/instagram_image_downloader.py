import pandas as pd
import json
import re
import os
import urllib.request
import datetime as dt

def ig_img_downloader(keyword):
    path = 'data/'+keyword+'/'

    directory = os.path.join(path, 'instagram_img')
    if not os.path.exists(directory):
        os.makedirs(directory)

    instagram = pd.read_csv(path + keyword +'_instagram_posts.csv')
    instagram = instagram[instagram['time_crawled'].notnull()]
    def check_day(date_str):
        current_time = dt.datetime.today()
        date = dt.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
        return (current_time-date).days == 0
    instagram_pic = instagram[instagram['time_crawled'].apply(check_day)][pd.notnull(instagram['image_versions2_candidates'])]
    i=0
    for id, post in enumerate(instagram_pic['image_versions2_candidates']):
        pic_json = json.loads(post.replace("'", "\""))
        #link = re.search('.*.jpg', pic_json[0]['url']).group(0)
        link = pic_json[0]['url']
        img_name = str(instagram_pic['pk'].iloc[id]) + '.jpg'
        #print(link, img_name)
        try:
            urllib.request.urlretrieve(link, directory + "/" + img_name)
            i+=1
        except:
            pass
        
        if i % 500 == 0:
            print( "%s Pictures downloaded: %s" % (i, dt.datetime.now()) )
    
    print('Done! %s Pictures downloaded' % i)


if __name__ == "__main__":
    main()
