import json
from re import L
from requests.api import get
import logging
from retrieve_config_data import news_apikey
from retrieve_config_data import covid_terms

def news_API_request(covid_terms = covid_terms):
    """argument string
    the phrases which to retreive articles with from the api
    
    gets news articles from the api which contain the correct terms
    
    return list(dictionary)
    the correct news articles from api
    """
    key = news_apikey ##change this through config
    url = 'https://newsapi.org/v2/everything?q=' + covid_terms + "&apiKey=" + key
    
    logging.info("getting data from api")
    data = get(url).json()['articles']
    logging.info("got data from api")

    return data
    
    ##key : 447b46b598644e9c83d9f2ae23b1ba20
    ##note when submitting put insert api key here in the config file

def update_news(covid_terms = covid_terms, articles = []):
    """argument list(dictionary)

    recalls the api and updates the news articles

    return list(dictionary)
    updated list of news articles
    """
    for art in news_API_request(covid_terms):
        try:
            articles.append(art)
        except:
            logging.error("articles is not callable")
            logging.debug("type of articles is" + str(type(articles)))

    return  articles