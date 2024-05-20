import json
import nltk
import mysql.connector
import statistics as stats

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer

with open('config.json') as f:
    config = json.load(f)

def prepare_text(string):

    tokens = nltk.word_tokenize(string.lower())
    
    stop_words = set(nltk.corpus.stopwords.words('english'))
    filtered_tokens  = [token for token in tokens if token not in stop_words]

    WNL = WordNetLemmatizer()

    lemmatized_tokens = [WNL.lemmatize(token) for token in filtered_tokens]

    prepared_string = ' '.join(lemmatized_tokens)
    return prepared_string


def get_sql_conn():
    
    connection = mysql.connector.connect(
        user=config['mysql']['username'],
        password=config['mysql']['password'],
        host=config['mysql']['hostname'],
        database=config['mysql']['database']
    )
    cursor = connection.cursor()
    
    return cursor


def analyze_user(userid):

    cursor = get_sql_conn()
    sia = SentimentIntensityAnalyzer()

    cursor.execute(f"SELECT m_content FROM userMessages WHERE c_id != 836834539837456436 AND m_sender = {userid} AND LENGTH(m_content) - LENGTH(REPLACE(m_content, ' ', '')) + 1 >= 5;")

    messages = cursor.fetchall()
    messageCount = len(messages)
    sentiments = []
    positiveMessages = 0

    for i, message, in enumerate(messages):
        sentiment = sia.polarity_scores(prepare_text(message[0]))
        sentiments.append(sentiment)
        if sentiment['pos'] > 0:
            positiveMessages += 1

    neg = f"{int(round(stats.mean([d['neg'] for d in sentiments]), 2)*100)}%"
    pos = f"{int(round(stats.mean([d['pos'] for d in sentiments]), 2)*100)}%"

    output = {
        "negative": neg,
        "positive": pos,
        "scanned_message": messageCount,
        "postitive_messages": positiveMessages
    }

    return output