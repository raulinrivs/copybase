import requests

def news_api_request():
    url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=f506b3ecb7944dd2bc890da434625323')
    return requests.get(url).json()
