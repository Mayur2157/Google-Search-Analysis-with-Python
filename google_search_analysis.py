import os
import pandas as pd
import plotly.express as px
import plotly.io as pio
from flask import Flask, render_template, request
from googleapiclient.discovery import build
from textblob import TextBlob
from collections import defaultdict, Counter

app = Flask(__name__)

# Google Custom Search API
API_KEY = 'AIzaSyD31p0SaRzsgDukTXeNfh2-VUFgFkr0dMM'
CSE_ID = '05cbd35a1cb374715'

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res

def render_table_html(df):
    html = df.to_html(classes='data', index=False, escape=False)
    clean_html = html.replace('\n ', '\n').replace('\n\n', '\n').strip()
    return clean_html

def get_keyword_frequency(results, keywords):
    keyword_freq = defaultdict(lambda: {'title': 0, 'snippet': 0})
    for item in results:
        title = item.get('title', '').lower()
        snippet = item.get('snippet', '').lower()
        for keyword in keywords:
            if keyword in title:
                keyword_freq[keyword]['title'] += 1
            if keyword in snippet:
                keyword_freq[keyword]['snippet'] += 1
    return keyword_freq

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    keywords = query.lower().split()  # Keywords to track
    results = google_search(query, API_KEY, CSE_ID, num=10).get('items', [])

    titles = [result['title'] for result in results]
    snippets = [result['snippet'] for result in results]
    
    df = pd.DataFrame({'Title': titles, 'Snippet': snippets})

    keyword_freq = get_keyword_frequency(results, keywords)
    keyword_freq_df = pd.DataFrame.from_dict(keyword_freq, orient='index').reset_index()
    keyword_freq_df.columns = ['Keyword', 'Title Frequency', 'Snippet Frequency']

    tables_html = render_table_html(df)
    keyword_freq_html = render_table_html(keyword_freq_df)

    sentiments = [TextBlob(snippet).sentiment.polarity for snippet in snippets]
    sentiment_labels = ['positive' if s > 0 else 'negative' if s < 0 else 'neutral' for s in sentiments]
    sentiment_counts = Counter(sentiment_labels)

    sentiment_plot = plot_sentiment_analysis(sentiment_labels)
    keyword_freq_plot = plot_keyword_frequency(keyword_freq_df)

    return render_template('results.html', tables=tables_html, keyword_freq=keyword_freq_html, sentiment_plot=sentiment_plot, keyword_freq_plot=keyword_freq_plot, sentiment_counts=sentiment_counts)

def plot_sentiment_analysis(sentiments):
    df = pd.DataFrame({'sentiment': sentiments})
    fig = px.histogram(df, x='sentiment', title='Sentiment Analysis of Search Results', labels={'sentiment':'Sentiment', 'count':'Count'})
    fig.update_layout(bargap=0.2)
    return pio.to_html(fig, full_html=False)

def plot_keyword_frequency(keyword_freq_df):
    fig = px.bar(keyword_freq_df, x='Keyword', y=['Title Frequency', 'Snippet Frequency'], title='Keyword Frequency in Titles and Snippets')
    fig.update_layout(barmode='group')
    return pio.to_html(fig, full_html=False)

if __name__ == '__main__':
    app.run(debug=True)
