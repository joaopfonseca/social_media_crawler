# =============================================================================
# https://www.kaggle.com/ngyptr/python-nltk-sentiment-analysis/notebook
# =============================================================================

#import csv
import pandas as pd

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.corpus import opinion_lexicon
import nltk.tokenize as tk
from unicodedata import normalize
import mtranslate

def to_string(message):
    return str(message)

def emoji_tokenize(message):
    emoji = "['\U0001F300-\U0001F5FF'|'\U0001F600-\U0001F64F'|'\U0001F680-\U0001F6FF'|'\u2600-\u26FF\u2700-\u27BF']"
    return tk.regexp_tokenize(message,emoji)

def hashtag_tokenize(message):
    hashtag = r"([#]\w+)"
    return tk.regexp_tokenize(message,hashtag)

#this tokenizer also removes hashtags and emojis (it only includes actual text content)
def message_tokenize(message):
    tweettokenizer = tk.TweetTokenizer()
    hashtag = r"([#]\w+)"
    hashtag_list = tk.regexp_tokenize(message,hashtag)
    emoji = "['\U0001F300-\U0001F5FF'|'\U0001F600-\U0001F64F'|'\U0001F680-\U0001F6FF'|'\u2600-\u26FF\u2700-\u27BF']"
    emoji_list = tk.regexp_tokenize(message,emoji)
    to_exclude_list = hashtag_list + emoji_list
    tokenized_message = tweettokenizer.tokenize(message)
    tokens = []
    for token in tokenized_message:
        if token not in to_exclude_list:
            tokens.append(token)
    return tokens

#normalizing function, removing uppercase, removing special characters etc. this will probably not be necessary
def normalize_text(txt):
    return normalize('NFKD', txt).encode('ASCII','ignore').decode('UTF-8').lower()




df = pd.read_csv(open('cascais_tweets.csv','r'))


def remove_stopwords(token_list):
    #removing stopwords (words which do not contain important significance to be used in Search Queries( the, for, this etc. ))
    filtered_words=[]
    for token in token_list:
        if token not in stopwords.words('english'):
            filtered_words.append(token)
    token_list = filtered_words
    return token_list

def positive_message_score(token_list):
    positive_words_list = opinion_lexicon.positive()
    positive_count = 0
    word_count = len(token_list)
    for token in token_list:
        if token in positive_words_list:
            positive_count=positive_count+1
    if word_count == 0:
        return ''
    else:
        return positive_count/word_count

def negative_message_score(token_list):
    negative_words_list = opinion_lexicon.negative()
    negative_count = 0
    word_count = len(token_list)
    for token in token_list:
        if token in negative_words_list:
            negative_count=negative_count+1
    if word_count == 0:
        return ''
    else:
        return negative_count/word_count

def VADER_analysis(message):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(message)



df['hashtags']=df['text'].apply(to_string).apply(normalize_text).apply(hashtag_tokenize)
df['emojis']=df['text'].apply(to_string).apply(emoji_tokenize)
df['message_english']=df['text'].apply(to_string).apply(mtranslate.translate)
df['tokenized']=df['message_english'].apply(message_tokenize).apply(remove_stopwords)
df['positive_score'] = df['tokenized'].apply(positive_message_score)
df['negative_score'] = df['tokenized'].apply(negative_message_score)
df['VADER_compound_score'] = df['message_english'].apply(VADER_analysis)

df[['text','tokenized','hashtags','emojis','positive_score','negative_score','VADER_compound_score']].to_csv('sentiment_analysis_test.csv')






