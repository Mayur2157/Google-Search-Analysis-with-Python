# Google-Search-Analysis-with-Python

This project is a web application built using Flask that allows users to perform Google searches and analyze the results. The analysis includes sentiment analysis and keyword frequency visualization using Plotly for interactive charts.

Features
Perform Google searches using the Custom Search JSON API.
Display search results in a tabular format.
Analyze the sentiment of the search results (positive, negative, neutral).
Visualize keyword frequency in the search results.
Interactive charts and graphs using Plotly.
Requirements
Python 3.7+
Flask
Google API Client
Pandas
Plotly
TextBlob

# Installation

Clone the repository:
git clone https://github.com/Mayur2157/Google-Search-Analysis-with-Python
cd google-search-analysis

Create and activate a virtual environment:
python -m venv search_analysis_env
search_analysis_env\Scripts\activate 

Install the required packages:
pip install -r requirements.txt

Set up your Google Custom Search API credentials:
Go to the Google Cloud Console.
Create a new project.
Enable the Custom Search JSON API.
Create an API key and Custom Search Engine ID (CSE_ID).
Add your API key and CSE ID to the code:
