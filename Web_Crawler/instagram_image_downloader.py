import pandas as pd
import json
import re
import os
import urllib.request


def ig_img_downloader(keyword):
    path = '_data/'

    directory = os.path.join(path, keyword+'_instagram_img')
    if not os.path.exists(directory):
        os.makedirs(directory)


    instagram = pd.read_csv(path + keyword +'_instagram_posts.csv')
    instagram_pic = instagram[pd.notnull(instagram['image_versions2_candidates'])]
    for id, post in enumerate(instagram_pic['image_versions2_candidates']):
        pic_json = json.loads(post.replace("'", "\""))
        link = re.search('.*.jpg', pic_json[0]['url']).group(0)
        img_name = str(instagram_pic['pk'].iloc[id]) + '.jpg'
        #print(link, img_name)
        try:
            urllib.request.urlretrieve(link, directory + "/" + img_name)
        except:
            pass

if __name__ == "__main__":
    main()
