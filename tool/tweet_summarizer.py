import string
import nltk
from nltk.tokenize import word_tokenize


class TweetSummarizer:
    def __init__(self):
        self.full_tweets = []               # stores each full tweet in a list of lists
        self.clean_tweets = []              # stores each cleaned tweet in a list of lists
        self.full_tweet_list = []           # stores each full tweet in a single list, each element being a tweet
        self.word_frequency_table = dict()  #
        self.tweet_value = dict()           #
        self.summary = ''
        self.average = 0

    def store_tweets(self):                 # check names of variables
        for line in open('tweets.csv'):
            row = line.split()
            clean_row = ''
            clean_row_list = []
            for word in row:
                clean_row = word
                clean_row = ''.join(hi for hi in clean_row if hi not in string.punctuation)
                clean_row_list.append(clean_row)
            self.clean_tweets.append(clean_row_list)
        self.clean_tweets.pop()

    def store_full_tweets(self, row):
        self.full_tweets.append(row)

    def generate_word_frequency_table(self):            # ASK IF ITS OK TO FOLLOW TUTORIAL
        ps = nltk.stem.porter.PorterStemmer()
        tweets = []
        individual_tweet = ''
        for tweet in self.full_tweets:
            # print(tweet)
            try:
                if tweet[0] == 'b':
                    tweet.pop(0)
                if tweet[0] == 'rt':
                    tweet.pop(0)
                if tweet[0] == "b'rt":
                    tweet.pop(0)
                if tweet[0] == "''":
                    tweet.pop(0)
                if tweet[0] == "'":
                    tweet.pop(0)
            except IndexError:
                print('Index Error')
            # returns a list of each tweet, now need to loop through it based on length and add to string. when length
            # is reached add to list and set individual to nothing
            temp_tweet_list = []
            for i in range(0, len(tweet)):
                individual_tweet += tweet[i] + ' '
            tweets.append(individual_tweet)
            individual_tweet = ''
        # transfer full tweets list of lists to a single list and use that for loop
        self.full_tweet_list = tweets
        for words in self.clean_tweets:
            for word in words:
                word = ps.stem(word)
                if word in self.word_frequency_table:
                    self.word_frequency_table[word] += 1
                else:
                    self.word_frequency_table[word] = 1

    def score_tweets(self):
        for tweet in self.full_tweet_list:
            tweet_word_count = len(word_tokenize(tweet))
            for word_value in self.word_frequency_table:
                if word_value in tweet:
                    if tweet in self.tweet_value:
                        self.tweet_value[tweet] += self.word_frequency_table[word_value]
                    else:
                        self.tweet_value[tweet] = self.word_frequency_table[word_value]
            try:
                self.tweet_value[tweet] = self.tweet_value[tweet] // tweet_word_count
            except ZeroDivisionError:
                continue

    def average_score(self):
        sum_values = 0
        for score in self.tweet_value:
            sum_values += self.tweet_value[score]

        self.average = int(sum_values / len(self.tweet_value))      # change some stuff

    def generate_summary(self):
        num_of_sentences = 0
        for tweet in self.full_tweet_list:
            if tweet in self.tweet_value and self.tweet_value[tweet] > (2 * self.average):  # change threshold
                self.summary += '\n' + tweet
                num_of_sentences += 1
                if num_of_sentences > 2:    # get input from user to how many tweets they want
                    break
