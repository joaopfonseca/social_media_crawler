import facebook
from urllib import request
import json
import datetime
import time


def facebook_page_search(keyword, access_token):
    query_type='page'
    def graph():
        return facebook.GraphAPI(access_token= access_token, version="2.10")

    page_search = graph().search(type=query_type, q=keyword)


    def request_until_succeed(url):
        req = request.Request(url)
        success = False
        while success is False:
            try:
                response = request.urlopen(req)
                if response.getcode() == 200:
                    success = True
            except Exception as e:
                print (e)
                time.sleep(5)

                print ("Error for URL %s: %s" % (url, datetime.datetime.now()))

        return response.read()

    def getnextlistofpages(url):
        data = json.loads(request_until_succeed(url))
        return data


    pages_id_list = []
    i=0
    while 0==0:
        try:
            try:
                pages_id_list.append( page_search['data'][i]['id'] )
                i=i+1
            except IndexError:
                page_search= getnextlistofpages(page_search['paging']['next'])
                i=0
        except KeyError:
            break


    return pages_id_list
