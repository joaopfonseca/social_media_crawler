
from flask import Flask, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import BadRequest
import update_manager
import os
#import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def homepage():
    pagetype = 'home'
    title = 'Welcome to the pre-alpha SMC GUI/Dashboard'
    paragraph = ['Hi there, this is a GUI under development for my social media crawler project!', '', 'Soon this page will have hyperlinks to dashboards of the 3 social media channels, direct interaction with the software, and an explation of how the overall project works. Stay tuned!']
    ############################################################################
    #values for keywords set in /support
    kw_settings=open('support/keywords_config', 'r')
    kws=kw_settings.readlines()
    keyword_1=kws[0]
    keyword_2=kws[1]
    keyword_3=kws[2]
    kw_settings.close()
    ############################################################################
    #getting active keyword
    if request.method == "POST":
        active_keyword = request.form['nav_keyword']
        with open('support/active_keyword', 'w') as kw_filter:
            kw_filter.write(active_keyword)
        #time.sleep(6)
    with open('support/active_keyword', 'r') as kw_filter:
        header_keyword=kw_filter.readline()
    ############################################################################

    return render_template('homepage.html', pagetype=pagetype,
                            keyword_1=keyword_1,
                            keyword_2=keyword_2,
                            keyword_3=keyword_3,
                            header_keyword=header_keyword)

@app.route('/config/', methods=['GET', 'POST'])
def config():
    pagetype = 'config'
    #values for keywords set in page /config
    kw_settings=open('support/keywords_config', 'r')
    kws=kw_settings.readlines()
    keyword_1=kws[0].strip()
    keyword_2=kws[1].strip()
    keyword_3=kws[2].strip()
    kw_settings.close()
    ############################################################################

    if request.method == "POST":
        ########################################################################
        #set active keyword:
        try:
            active_keyword = request.form['nav_keyword']
            with open('support/active_keyword', 'w') as kw_filter:
                kw_filter.write(active_keyword)
            #time.sleep(6)
        except BadRequest as e:
            pass
        ########################################################################
        #configre keywords:
        try:
            if request.form['keyword_1'] == '':
                pass
            else:
                keyword_1 = request.form['keyword_1']

            if request.form['keyword_2'] == '':
                pass
            else:
                keyword_2 = request.form['keyword_2']

            if request.form['keyword_3'] == '':
                pass
            else:
                keyword_3 = request.form['keyword_3']

            with open('support/keywords_config', 'w') as update_kw_configs:
                update_kw_configs.write(keyword_1+'\n')
                update_kw_configs.write(keyword_2+'\n')
                update_kw_configs.write(keyword_3)
            flash('Keyword 1 is set to \'%s\'' % keyword_1)
            flash('Keyword 2 is set to \'%s\'' % keyword_2)
            flash('Keyword 3 is set to \'%s\'' % keyword_3)
        except BadRequest as e:
            pass
        ########################################################################
        #Update Manager here

        try:
            kw_nmbr = request.form['crawler']
            flash('Launching Batch Crawler/Scheduled Updater for keyword \'%s\'' % keyword_1)
            update_manager.auto_crawler(keyword_1)
        except BadRequest as e:
            pass

        try:
            kw_nmbr = request.form['twitter']
            if kw_nmbr == "1":
                twt_keyword=keyword_1
            elif kw_nmbr == "2":
                twt_keyword=keyword_2
            elif kw_nmbr == "3":
                twt_keyword=keyword_3
            flash('Updated Twitter for keyword \'%s\'' % twt_keyword)
            update_manager.kw_twitter_updater(twt_keyword,int(kw_nmbr))
        except BadRequest as e:
            pass

        try:
            kw_nmbr = request.form['facebook']
            if kw_nmbr == "1":
                fb_keyword=keyword_1
            elif kw_nmbr == "2":
                fb_keyword=keyword_2
            elif kw_nmbr == "3":
                fb_keyword=keyword_3
            flash('Updated Facebook for keyword \'%s\'' % fb_keyword)
            update_manager.kw_fb_updater(fb_keyword,int(kw_nmbr))
        except BadRequest as e:
            pass

        try:
            kw_nmbr = request.form['instagram']
            if kw_nmbr == "1":
                ig_keyword=keyword_1
            elif kw_nmbr == "2":
                ig_keyword=keyword_2
            elif kw_nmbr == "3":
                ig_keyword=keyword_3

            flash('Updated Instagram for keyword \'%s\'' % ig_keyword)
            update_manager.kw_instagram_updater(ig_keyword,int(kw_nmbr))
        except BadRequest as e:
            pass

        try:
            kw_nmbr = request.form['ig_img']
            if kw_nmbr == "1":
                img_keyword=keyword_1
            elif kw_nmbr == "2":
                img_keyword=keyword_2
            elif kw_nmbr == "3":
                img_keyword=keyword_3
            flash('Crawled Instagram Images for keyword \'%s\'' % img_keyword)
            update_manager.instagram_img_downloader(img_keyword)
        except BadRequest as e:
            pass

        ########################################################################

    ############################################################################
    #getting active keyword
    with open('support/active_keyword', 'r') as kw_filter:
        header_keyword=kw_filter.readline()
    ############################################################################
    title = 'SMC Control Panel'

    return render_template('config_page.html',
                            title = title,
                            pagetype=pagetype,
                            keyword_1=keyword_1,
                            keyword_2=keyword_2,
                            keyword_3=keyword_3,
                            header_keyword=header_keyword
                            )

@app.route('/facebook/', methods=['GET', 'POST'])
def facebookpage():
    pagetype = 'facebook'
    port = 'http://127.0.0.1:8050/'
    ############################################################################
    #getting active keyword
    if request.method == "POST":
        active_keyword = request.form['nav_keyword']
        with open('support/active_keyword', 'w') as kw_filter:
            kw_filter.write(active_keyword)
        #time.sleep(6)
    with open('support/active_keyword', 'r') as kw_filter:
        header_keyword=kw_filter.readline()
    ############################################################################
    #values for keywords set in /support
    kw_settings=open('support/keywords_config', 'r')
    kws=kw_settings.readlines()
    keyword_1=kws[0]
    keyword_2=kws[1]
    keyword_3=kws[2]
    kw_settings.close()
    ############################################################################
    return render_template('dashboard.html', port=port, pagetype=pagetype,
                            keyword_1=keyword_1,
                            keyword_2=keyword_2,
                            keyword_3=keyword_3,
                            header_keyword=header_keyword)

@app.route('/instagram/', methods=['GET', 'POST'])
def Instagrampage():
    pagetype = 'instagram'
    port = 'http://127.0.0.1:8051/'
    ############################################################################
    #getting active keyword
    if request.method == "POST":
        active_keyword = request.form['nav_keyword']
        with open('support/active_keyword', 'w') as kw_filter:
            kw_filter.write(active_keyword)
        #time.sleep(6)
    with open('support/active_keyword', 'r') as kw_filter:
        header_keyword=kw_filter.readline()
    ############################################################################
    #values for keywords set in /support
    kw_settings=open('support/keywords_config', 'r')
    kws=kw_settings.readlines()
    keyword_1=kws[0]
    keyword_2=kws[1]
    keyword_3=kws[2]
    kw_settings.close()
    ############################################################################
    #values for keywords set in /support
    kw_settings=open('support/keywords_config', 'r')
    kws=kw_settings.readlines()
    keyword_1=kws[0]
    keyword_2=kws[1]
    keyword_3=kws[2]
    kw_settings.close()
    ############################################################################
    return render_template('dashboard.html', port=port, pagetype=pagetype,
                            keyword_1=keyword_1,
                            keyword_2=keyword_2,
                            keyword_3=keyword_3,
                            header_keyword=header_keyword)

@app.route('/twitter/', methods=['GET', 'POST'])
def twitterpage():
    pagetype = 'twitter'
    port = 'http://127.0.0.1:8052/'
    ############################################################################
    #getting active keyword
    if request.method == "POST":
        active_keyword = request.form['nav_keyword']
        with open('support/active_keyword', 'w') as kw_filter:
            kw_filter.write(active_keyword)
        #time.sleep(6)
    with open('support/active_keyword', 'r') as kw_filter:
        header_keyword=kw_filter.readline()
    ############################################################################
    #values for keywords set in /support
    kw_settings=open('support/keywords_config', 'r')
    kws=kw_settings.readlines()
    keyword_1=kws[0]
    keyword_2=kws[1]
    keyword_3=kws[2]
    kw_settings.close()
    ############################################################################
    return render_template('dashboard.html', port=port, pagetype=pagetype,
                            keyword_1=keyword_1,
                            keyword_2=keyword_2,
                            keyword_3=keyword_3,
                            header_keyword=header_keyword)

if __name__ == '__main__':
    app.secret_key = 'mom cooks the best lasagna'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port=5000)
