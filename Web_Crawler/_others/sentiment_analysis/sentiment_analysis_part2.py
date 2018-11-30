from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

df = pd.read_csv(open('sentiment_analysis_test.csv', 'r'))


def VADER_analysis(message):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(message)

df['VADER_compound_score'] = df['message_english'].apply(VADER_analysis)

df.to_csv('sentiment_analysis_test2.csv')