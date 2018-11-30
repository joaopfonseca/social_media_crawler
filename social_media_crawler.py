import os
import subprocess
import sys
import time


project_dir = os.path.realpath('')
gui = '/gui/FlaskApp/'

os.chdir(project_dir+gui)

f = subprocess.Popen(['python','db_facebook.py'])
i = subprocess.Popen(['python','db_instagram.py'])
t = subprocess.Popen(['python','db_twitter.py'])
gui = subprocess.Popen(['python','__init__.py'])

time.sleep(3)
os.system('open http://0.0.0.0:5000/')

kw_file = open('support/active_keyword','r')
active_keyword = kw_file.readline()
keyword = active_keyword.rstrip()
kw_file.close()

while True:
    kw_file2 = open('support/active_keyword','r')
    active_keyword2 = kw_file2.readline()
    keyword2 = active_keyword2.rstrip()
    kw_file2.close()
    if keyword != keyword2:
        f.terminate()
        i.terminate()
        t.terminate()
        keyword=keyword2
        f = subprocess.Popen(['python','db_facebook.py'])
        i = subprocess.Popen(['python','db_instagram.py'])
        t = subprocess.Popen(['python','db_twitter.py'])
