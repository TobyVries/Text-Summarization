import sys
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from tool.long import LongSummarizer
from tool.tweet_summarizer import TweetSummarizer
from sumy.models.dom._sentence import Sentence
from sumy.nlp.tokenizers import Tokenizer
from sumy.evaluation.rouge import rouge_1
from nltk.twitter import Twitter, Query, TweetViewer, TweetWriter, credsfromfile
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import csv
import re
from tool.scraper import Scraper


def store_article(txt):
    f = open("document.txt", "w")
    for item in txt:
        f.write(item)
    f.close()


def calculate_rouge_1_score(summary):
    scores = []
    average = 0
    k = 0
    ideal_summary_1 = 'Jason saw a nice weather forecast and went to the beach with his kids for 2 hours.'
    ideal_summary_2 = 'Jason took the kids swimming at the beach on a sunny day.'
    ideal_summary_3 = 'Jason decided to take the kids to the beach since it was a sunny day.'
    ideal_summaries = [ideal_summary_1, ideal_summary_2, ideal_summary_3]
    tokenizer = Tokenizer('english')
    summary_sentence = Sentence(summary, tokenizer)
    for s in ideal_summaries:
        ideal_sentence = Sentence(ideal_summaries[k], tokenizer)
        scores.append(rouge_1([summary_sentence], [ideal_sentence]))
        average += scores[k]
        k += 1
    scores.append(average/3)
    return scores


def clean_text(t):
    unwanted_char = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'
    t = "".join([(" " if n in unwanted_char else n) for n in text if n not in unwanted_char])
    return t


def clean_tweet(tweet_text):
    stop_words = stopwords.words('english')
    tweet_text = re.sub(r'(?:\@|https?\://)\S+', '', str(tweet_text))   # remove links and @
    #tweet_text = re.sub(r'\\', '', str(tweet_text))
    # tweet_text = tweet_text.strip("\\")
    # tweet_text = tweet_text.replace("\\", "")
    tweet_text = word_tokenize(str(tweet_text).lower(), 'english')      # tokenize words and make lower case
    #tweetSummarizer.store_full_tweets(tweet_text)          #MAY BREAK SOMETHING
    clean_tweet_text = []
    filtered_tweet_text = [word for word in tweet_text if word.isalpha()]   # remove non-alpha values
    for word in filtered_tweet_text:
        if word not in stop_words:
            clean_tweet_text.append(word)
    try:
        if clean_tweet_text[0] == 'b':
            clean_tweet_text.pop(0)
        if clean_tweet_text[0] == 'rt':
            clean_tweet_text.pop(0)
    except IndexError:
        print('error')
    return clean_tweet_text


rouge_paragraph = 'Jason listened to the weather and heard it was going to be sunny. He thought the kids might like ' \
                  'to go swimming. He gathered up the swimsuits, \ntowels and sunscreen. Jason and the kids got into ' \
                  'the truck and drove to the beach. They spent the next 2 hours playing and splashing in the surf.\n'
rouge_textrank_summary = 'Jason and the kids got into the truck and drove to the beach.'
rouge_lexrank_summary = 'Jason listened to the weather and heard it was going to be sunny.'
rouge_lsa_summary = 'He thought the kids might like to go swimming.'
rouge_kl_sum_summary = 'Jason and the kids got into the truck and drove to the beach.'
rouge_luhn_summary = 'Jason and the kids got into the truck and drove to the beach.'
rouge_sumbasic_summary = 'Jason and the kids got into the truck and drove to the beach.'

text = []
while True:
    choice = input("Do you want to: \n1. Summarize an article\n2. Summarize a twitter topic\n3. Display the ROUGE "
                   "score for each algorithm\n4. Summarize a users tweets\n")
    try:
        choice_int = int(choice)
        if choice_int < 1 or choice_int > 4:
            print('Incorrect number entered. Try again.')
            continue
        else:
            break
    except ValueError:
        print('Invalid input. Enter either a 1, 2, 3 or 4 depending on what you would like to do.')
if choice == '1':   # summarize an article
    while True:  # Get the number of sentences that the user wants the article to be summarized to
        number = input("How many sentences\n")
        try:
            num_of_sentences = int(number)
            if num_of_sentences < 1:
                print("Invalid input, number of sentences needs to be between 1 and 20")
                continue
            elif num_of_sentences > 20:
                print("Invalid input, number of sentences needs to be between 1 and 20")
                continue
            break
        except ValueError:
            print("Invalid input, number of sentences needs to be a positive number of 20 or lower")
    while True:  # Get the number of sentences that the user wants the article to be summarized to
        number = input("Enter an article (1) or summarise from file (2) or enter url (3)?\n")
        try:
            file_or_keyboard_or_url = int(number)
            if file_or_keyboard_or_url < 1:
                print("Invalid input, pick either 1, 2 or 3.")
                continue
            elif file_or_keyboard_or_url > 3:
                print("Invalid input, pick either 1, 2 or 3.")
                continue
            break
        except ValueError:
            print("Invalid input, pick either 1, 2 or 3.")
    if file_or_keyboard_or_url == 1:        # Enter article
        print("Enter the article to summarized\n")
        while True:     # Get user input for article to be summarised
            try:
                line = input()
            except EOFError:
                break
            text.append(line)
        store_article(text)
        count_file = open("document.txt", "rt")
        data = count_file.read()
        total_word_count = data.split()
        file = "document.txt"
        parser = PlaintextParser.from_file(file, Tokenizer("english"))
    elif file_or_keyboard_or_url == 2:      # Document
        while True:
            print("Enter the location of the file\n")
            file = input()
            try:
                count_file = open(file, "rt")
                data = count_file.read()
                total_word_count = data.split()
                parser = PlaintextParser.from_file(file, Tokenizer("english"))
                break
            except FileNotFoundError:
                print('File not found at location entered.')
    elif file_or_keyboard_or_url == 3:      # URL
        scraper = Scraper()
        while len(text) == 0:
            url = str(input("Enter the URL of the BBC article.\n"))
            scraper.set_url(url)
            text = scraper.scrape_article()
        text_updated = [i.replace('£', '') for i in text]   # remove symbols which aren't utf-8
        store_article(text_updated)
        count_file = open("document.txt", "rt")
        data = count_file.read()
        total_word_count = data.split()
        file = "document.txt"
        parser = PlaintextParser.from_file(file, Tokenizer("english"))

    textrank = LongSummarizer("TextRank", TextRankSummarizer())
    lexrank = LongSummarizer("LexRank", LexRankSummarizer())
    lsa = LongSummarizer("LSA", LsaSummarizer())
    kl_sum = LongSummarizer("KL-Sum", KLSummarizer())
    luhn = LongSummarizer("Luhn", LuhnSummarizer())
    sumbasic = LongSummarizer("SumBasic", SumBasicSummarizer())

    textrank.create_summary(parser, num_of_sentences, total_word_count)
    lexrank.create_summary(parser, num_of_sentences, total_word_count)
    lsa.create_summary(parser, num_of_sentences, total_word_count)
    kl_sum.create_summary(parser, num_of_sentences, total_word_count)
    luhn.create_summary(parser, num_of_sentences, total_word_count)
    sumbasic.create_summary(parser, num_of_sentences, total_word_count)

    textrank.display_summary()
    lexrank.display_summary()
    lsa.display_summary()
    kl_sum.display_summary()
    luhn.display_summary()
    sumbasic.display_summary()

    print("\nTotal number of words: ", len(total_word_count))
    textrank.display_comparison()
    lexrank.display_comparison()
    lsa.display_comparison()
    kl_sum.display_comparison()
    luhn.display_comparison()
    sumbasic.display_comparison()

elif choice == '2':     # summarize a twitter topic
    tweet_topic = input("Enter the topic you want a summary for\n")

    # Authenticate and retrieve tweets based on user entered topic
    oauth = credsfromfile()
    client = Query(**oauth)
    client.register(TweetWriter())
    tweets = client.search_tweets(keywords=tweet_topic, limit=100, lang='en')

    tweetSummarizer = TweetSummarizer()

    # clean tweets and store in tweets.csv
    rows = []
    usable_rows = []
    for tweet in tweets:
        rows.append(str(tweet['text']))#.encode('utf-8')) # may need to add , 'ignore'
    if len(rows) > 0:
        usable_rows = rows.copy()
        for i in range(0, len(rows)):
            rows[i] = clean_tweet(rows[i])
            tweetSummarizer.store_full_tweets(rows[i])
        with open('tweets.csv', 'w', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter='\n')
            writer.writerow(rows)
        # print('before', usable_rows)
        for row in range(0, len(usable_rows)):
            usable_rows[row] = re.sub(r'(?:\@|https?\://)\S+', '', str(usable_rows[row]))  # remove links and @
            usable_rows[row] = re.sub(r'\bpic.twitter.com/\w+', '', str(usable_rows[row]))  # removes pic.twitter links
        # print('after', usable_rows)
        for row in range(0, len(usable_rows)):
            usable_rows[row] = usable_rows[row].replace("b'", "")
            usable_rows[row] = usable_rows[row].replace('b"', "")
            usable_rows[row] = usable_rows[row].replace("RT", "")
            usable_rows[row] = usable_rows[row].replace("\\n", "")
            usable_rows[row] = usable_rows[row].lstrip()
            clean_text(usable_rows[row])
        # print('after 2', usable_rows)
        tweetSummarizer.display_tweets = usable_rows
        tweetSummarizer.store_tweets()
        tweetSummarizer.generate_word_frequency_table()
        tweetSummarizer.score_tweets()
        tweetSummarizer.average_score()
        tweetSummarizer.generate_summary()
        print(tweetSummarizer.summary)

elif choice == '3':
    print('The paragraph to summarize was:\n', rouge_paragraph)

    rouge_1_scores = [
        [calculate_rouge_1_score(rouge_textrank_summary)],
        [calculate_rouge_1_score(rouge_lexrank_summary)],
        [calculate_rouge_1_score(rouge_lsa_summary)],
        [calculate_rouge_1_score(rouge_kl_sum_summary)],
        [calculate_rouge_1_score(rouge_luhn_summary)],
        [calculate_rouge_1_score(rouge_sumbasic_summary)]
    ]
    print('Score 1, 2, 3 and average are displayed')
    print('TextRank ROUGE 1 scores:', rouge_1_scores[0])
    print('LexRank ROUGE 1 scores:', rouge_1_scores[1])
    print('LSA ROUGE 1 scores:', rouge_1_scores[2])
    print('KL-Sum ROUGE 1 scores:', rouge_1_scores[3])
    print('Luhn ROUGE 1 scores:', rouge_1_scores[4])
    print('SumBasic ROUGE 1 scores:', rouge_1_scores[5])


elif choice == '4':     # summarize user tweets
    user = input("Enter the user handle.\n")
    scraper = Scraper()
    scraper.set_user_url(user)
    rows = scraper.scrape_user_tweets()
    if len(rows) == 0:
        print('No user with that name, or no tweets found.')
        sys.exit()
    summarizer = TweetSummarizer()
    for row in range(0, len(rows)):
        rows[row] = re.sub(r'(?:\@|https?\://)\S+', '', str(rows[row]))   # remove links and @
        rows[row] = re.sub(r'\bpic.twitter.com/\w+', '', str(rows[row]))  # removes pic.twitter links

    summarizer.display_tweets = rows

    clean_rows = scraper.scrape_user_tweets()
    for i in range(0, len(clean_rows)):
        clean_rows[i] = clean_tweet(clean_rows[i])
        summarizer.store_full_tweets(clean_rows[i])
    with open('tweets.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter='\n')
        writer.writerow(clean_rows)

    summarizer.store_tweets()
    summarizer.generate_word_frequency_table()
    summarizer.score_tweets()
    summarizer.average_score()
    summarizer.generate_summary()
    print(summarizer.summary)

# for testing record times and put in graph to ensure timing are correct
