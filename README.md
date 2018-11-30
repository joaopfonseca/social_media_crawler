
<p align="center">
  <img src="https://image.ibb.co/fZ87Yb/project_header.png" width="100%"/>
</p>
The aim of the project is to build a program that is able to get publicly available data regarding a specific keyword from the three main Social Media platforms: Facebook, Instagram and Twitter.

When using this tool, the end user will have access to all the data that is available from these channels regarding a specific topic of analysis (which can include up to 3 keywords), as well as an interactive dashboard containing an analysis of this data using traditional Business Intelligence procedures and visualisations. Future work will include Text Mining methods to analyse the content of the extracted text messages (work done towards this goal can be found in `Web_Crawler/_others/`).

## Prerequisites
### Software
#### Installing git and forking the repo
Fork a copy of this repository onto your own GitHub account and `clone` your fork of the repository onto your computer:

`git clone https://github.com/<your_github_username>/social_media_crawler.git`

(Currently this is a private repo, so this should not work unless you have access to the GitHub page)


#### Installing Python and setting up the virtual environment
[Install Python 3.6.3](https://www.python.org/downloads/release/python-363/) and the [conda package manager](https://conda.io/miniconda.html) (use miniconda, not anaconda, because we will install all the packages we need).

Navigate to the project directory inside a terminal and create a virtual environment (replace <environment_name>, for example, with "dssg") and install the [required packages](https://github.com/DSSG2017/social_media_crawler/blob/master/requirements.txt):

`conda create -n <environment_name> --file requirements.txt python=3.6.3`

Activate the virtual environment:

`source activate <environment_name>`

By installing these packages in a virtual environment, we avoid dependency clashes with other packages that may already be installed elsewhere on your computer.

### Set up Access Tokens
In order to properly use this tool, it will be necessary to create some access tokens to access the API's from Twitter and Facebook (Graph API), as well as create some Instagram accounts through which we will crawl data from.

#### Instagram
You will need to set up 3 Instagram accounts (https://www.instagram.com/). After that, insert the accounts' username and password in the script `Web_Crawler/instagram_access.py`.

#### Twitter
It is necessary to create 4 access tokens for Twitter API (https://apps.twitter.com/). Insert the generated API key, API secret, Access token and Access token secret for each created app in the script `Web_Crawler/twitter_tweets.py`.

#### Facebook
Multiple access tokens will be required (originally set to 23 tokens, although the need for more or less tokens will vary on the quality of the internet connection: the faster the connection, the more tokens will be necessary) to crawl relatively large amounts of data using Facebook's Graph API (https://developers.facebook.com/apps/).  Afterwards, insert the App ID and App Secret for each access token generated into the script `Web_Crawler/facebook_access_token.py`.

#### Mapbox
In order to use geographical visualisations for Instagram and Twitter data Mapbox will be used. For this, we will need one Access Token (https://www.mapbox.com/account/access-tokens). Insert the generated Access Token into `gui/FlaskApp/db_instagram.py` and `gui/FlaskApp/db_twitter.py` (variable is defined below the imports).

### Database

The data crawled with this tool is currently stored in various CSV files. Although, this is expected to be changed into an actual database.

## Graphical User Interface

The GUI was developed as a Web App using the Flask web framework, along with HTML markup and Bootstrap 4.0.0 templating. Visualisations were developed using the Plotly library, along with Plotly's Dash library.

From the GUI it is possible to configure active keywords, crawl data from the 3 social media channels (Facebook, Instagram and Twitter) and visualise the data that was stored from these sources using the Navbar to cycle through these functionalities. Other visualisations and data analysis using Text Mining methods will be added later on.

## How it works

The program is divided in 6 parts: collection of data from the 3 social media channels, for both collection of data in a batch and updating existing data.

### Facebook Crawler
Tools used: Facebook’s Graph API, Facebook-SDK Python Library

As Facebook restricted two years ago the crawling of posts published by individuals, this tool was directed to fetch data regarding Facebook Pages’ activities and user interactions with them. In order words, for each crawled Facebook page the program will store all the published posts (including content, creation date, ID etc.) by the page, each post’s like and share number, as well as its comments, including content and creation date. It has no restriction on post creation date, and virtually no restriction on the number of requests made per period of time.
After performing the first batch crawl (which will store all the historical data, tracing back to 2009), the data can be then updated regularly.
The posts that were crawled are associated to the Facebook page ID and the comments are also associated to the corresponding post’s ID.

The following diagram depicts the steps done in order to fetch data from posts in Facebook Pages and the comments linked to these posts:

<p align="center">
  <img src="http://svgur.com/i/5C1.svg" width="200"/>
</p>

Most relevant data stored (posts): Post ID, message, post type, creation date, likes count, comments count and shares count.
Most relevant data stored (comments): Post ID, Comment ID, Comment message and comment creation date.

### Twitter Crawler
Tools used: Twitter’s Search API, Tweepy Python Library

The program can crawl 2000 tweets every 15 minutes. After this, it is able to continuously update this data and append to the existing data new tweets containing a specified keyword. Although limited in what regards storing historical data, it is capable of storing a high amount of tweets very frequently, hence ensuring that the stored information is updated in nearly real time.

Most relevant data stored: Location Coordinates, Creation Date, Favourite Count, Tweet ID, Post Language, Location Name, Retweet Count, Tweet Message, User name, User description, User favourites count, User followers count, User friends count and User Location.

### Instagram Crawler
Tools used: Instagram-API-python Python Library

The program can crawl a maximum of approximately 2 250 Instagram posts each time it runs and is able to run every 15 minutes. It does not restrict the data being fetched by its publication date. However, the API does not allow to query according to the period of time we are interested in. Just like the previous Crawler, it can update very frequently, which allows data to be updated in near real time. It is also important to mention that the Crawler is also capable of downloading the pictures of each post being stored.

Most relevant data stored (posts): Creation time, post ID, Message, User Name, User ID, Image posted URL, like count, Video posted URL, View count, comment count, Location name, latitude and longitude


**For simplification purposes, a diagram demonstrating the program’s social media crawling process is presented:**

<p align="center">
  <img src="http://svgur.com/i/5D4.svg" width="320"/>
</p>

## Directory structure
```
social_media_crawler/
├── LICENSE
├── README.md
├── Web_Crawler
│   ├── InstagramAPI
│   ├── __init__.py
│   ├── _data
│   ├── _master.py
│   ├── _master_batch_crawler.py
│   ├── _others
│   ├── facebook
│   ├── facebook_access_token.py
│   ├── facebook_comments.py
│   ├── facebook_posts.py
│   ├── facebook_search_results.py
│   ├── instagram_hashtags.py
│   ├── instagram_image_downloader.py
│   ├── twitter_tweets.py
│   ├── update_fb_comments.py
│   ├── update_fb_posts.py
│   └── update_insta_hashtags.py
├── gui
│   └── FlaskApp
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── db_instagram.cpython-36.pyc
│       │   └── update_manager.cpython-36.pyc
│       ├── db_facebook.py
│       ├── db_instagram.py
│       ├── db_twitter.py
│       ├── static
│       ├── support
│       │   ├── active_keyword
│       │   └── keywords_config
│       ├── templates
│       │   ├── config_page.html
│       │   ├── dashboard.html
│       │   ├── header.html
│       │   └── homepage.html
│       └── update_manager.py
└── social_media_crawler.py
```

## Authors
This project was conducted as part of Data Science for Social Good 2018 (DSSG) fellowship, as well as part of João Fonseca's Master thesis for Nova School of Business and Economics' Masters in Management Double Degree program with Nova Information Management School's Master in Information Management (with specialisation in **Digital Business** and **Knowledge Management and Business Intelligence**, respectively).

**Developer**: João Fonseca

**Technical Mentor**: Qiwei Han

**Project/Thesis Advisor**: Professors Leid Zejnilović and Miguel Neto
