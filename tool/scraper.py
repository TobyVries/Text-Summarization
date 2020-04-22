from bs4 import BeautifulSoup
import requests
import sys
from requests.exceptions import MissingSchema


class Scraper:
    def __init__(self, url=None):
        self.url = url

    def scrape_article(self):
        text = []
        text_updated = []
        try:
            scrape = requests.get(self.url)
            soup = BeautifulSoup(scrape.text, 'html.parser')
            all_paragraphs = soup.find('div', {'class':'story-body__inner'})
            try:
                paragraph = all_paragraphs.find_all('p')
                for p in paragraph:
                    text.append(p.get_text() + " ")
                    text_updated = [i.replace('£', '') for i in text]  # remove symbols which aren't utf-8
            except AttributeError:
                print('Not a valid URL.')
                sys.exit()
        except MissingSchema:
            print('Not a valid URL.')
            return text
        return text_updated

    def scrape_tweets(self):
        text = []
        try:
            scrape = requests.get(self.url)
            soup = BeautifulSoup(scrape.content, 'html.parser')
            all_tweets = soup.find_all('p', {'class':'TweetTextSize TweetTextSize--jumbo js-tweet-text tweet-text'})
            for tweet in all_tweets:
                text.append(tweet.get_text())
        except MissingSchema:
            print('Not a valid URL.')
            return text
        return text

    def scrape_user_tweets(self):
        text = []
        try:
            scrape = requests.get(self.url)
            soup = BeautifulSoup(scrape.text, 'html.parser')
            all_tweets = soup.find_all('p', {'class':'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'})
            for tweet in all_tweets:
                text.append(tweet.get_text())
        except MissingSchema:
            print('Not a valid URL.')
            return text
        return text

    def set_url(self, url):
        self.url = url.strip()

    def set_user_url(self, user):
        self.url = "https://twitter.com/" + user.strip()
