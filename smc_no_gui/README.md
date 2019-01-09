
<p align="center">
  <img src="https://image.ibb.co/fZ87Yb/project_header.png" width="100%"/>
</p>
This is a second, more consistent version of the Social Media Crawler. It contains a simple Command-Line interface that allows more flexibility on the keywords to crawl and is much more stable than the the Graphical User Interface version. Due to Facebook API changes, so far no solution was found to crawl useful data from the platform. For this reason, this version crawls Twitter and Instagram only.

## Prerequisites
### Software
#### Installing git and forking the repo
Fork a copy of this repository onto your own GitHub account and `clone` your fork of the repository onto your computer:

`git clone https://github.com/<your_github_username>/social_media_crawler.git`


#### Installing Python and setting up the virtual environment
[Install Python 3.6.3](https://www.python.org/downloads/release/python-363/) and the [conda package manager](https://conda.io/miniconda.html) (use miniconda, not anaconda, because we will install all the packages we need).

Navigate to the project directory inside a terminal and create a virtual environment (replace <environment_name>, for example, with "dssg") and install the [required packages](https://github.com/DSSG2017/social_media_crawler/blob/master/requirements.txt):

`conda create -n <environment_name> --file requirements.txt python=3.6`

Activate the virtual environment:

`source activate <environment_name>`

By installing these packages in a virtual environment, we avoid dependency clashes with other packages that may already be installed elsewhere on your computer.

### Set up Access Tokens
In order to properly use this tool, it will be necessary to create some access tokens to access the API's from Twitter and as many Instagram accounts as keywords one desires to crawl simultaneously.

#### Instagram
You will need to set up at least one Instagram accounts (https://www.instagram.com/). After that, insert the accounts' username and password in the script `creds.py`.

#### Twitter
It is necessary to create at least 1 app access for Twitter API (https://apps.twitter.com/). Insert the generated API key, API secret, Access token and Access token secret for each created app in the script `creds.py`.

### Database

The data crawled with this tool is currently stored in various CSV files. Although, this is expected to be changed into an actual database.

## How it works

The program is divided in 4 parts: collection of data in a batch and updating existing data from the 2 social media channels.
<br>
Start by running the script `smc_no_gui.py`. Two arguments are required: `-creds_id` and `-keyword`:
- `creds_id`: ID (number) of the set of credentials to use. You can update this list in the file `creds.py`
- `-keyword`: Keyword to crawl

<br></br>

**Example:** `python path_to_project_folder/smc_no_gui.py -creds_id 1 -keyword cascais`
<br>
That's it! The program will run continuously unless interrupted with scheduled updates and store the data in the folder `data`.
<br>
### Twitter Crawler
Tools used: Twitter’s Search API, Tweepy Python Library

The program can crawl 2000 tweets every 15 minutes. After this, it is able to continuously update this data and append to the existing data new tweets containing a specified keyword. Although limited in what regards storing historical data, it is capable of storing a high amount of tweets very frequently, hence ensuring that the stored information is updated in nearly real time.

Most relevant data stored: Location Coordinates, Creation Date, Favourite Count, Tweet ID, Post Language, Location Name, Retweet Count, Tweet Message, User name, User description, User favourites count, User followers count, User friends count and User Location.

### Instagram Crawler
Tools used: Instagram-API-python Python Library

The program can crawl a maximum of approximately 2 250 Instagram posts each time it runs and is able to run every 15 minutes. It does not restrict the data being fetched by its publication date. However, the API does not allow to query according to the period of time we are interested in. Just like the previous Crawler, it can update very frequently, which allows data to be updated in near real time. It is also important to mention that the Crawler is also capable of downloading the pictures of each post being stored.

Most relevant data stored (posts): Creation time, post ID, Message, User Name, User ID, Image posted URL, like count, Video posted URL, View count, comment count, Location name, latitude and longitude

## Directory structure
```
smc_no_gui
├── README.md
├── creds.py
├── data
├── requirements.txt
├── smc_no_gui.py
└── src
    ├── InstagramAPI
    ├── __init__.py
    ├── instagram_hashtags.py
    ├── instagram_image_downloader.py
    ├── twitter_tweets.py
    └── update_insta_hashtags.py
```

## Authors
- João Fonseca
- Lénia Mestrinho
- Leid Zejnilović

