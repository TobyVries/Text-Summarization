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


def clean_tweet(tweet_text):
    stop_words = stopwords.words('english')
    tweet_text = re.sub(r'(?:\@|https?\://)\S+', '', str(tweet_text))   # remove links and @
    #tweet_text = re.sub(r'\\', '', str(tweet_text))
    # tweet_text = tweet_text.strip("\\")
    # tweet_text = tweet_text.replace("\\", "")
    tweet_text = word_tokenize(str(tweet_text).lower(), 'english')      # tokenize words and make lower case
    tweetSummarizer.store_full_tweets(tweet_text)
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
                  'the truck and drove to the beach. They spent the next 2 hours playing and splashing in the surf.'
rouge_textrank_summary = 'Jason and the kids got into the truck and drove to the beach.'
rouge_lexrank_summary = 'Jason listened to the weather and heard it was going to be sunny.'
rouge_lsa_summary = 'He thought the kids might like to go swimming.'
rouge_kl_sum_summary = 'Jason and the kids got into the truck and drove to the beach.'
rouge_luhn_summary = 'Jason and the kids got into the truck and drove to the beach.'
rouge_sumbasic_summary = 'Jason and the kids got into the truck and drove to the beach.'

text = []
while True:
    choice = input("Do you want to: \n1. Summarize an article\n2. Summarize a twitter topic\n3. Display the ROUGE "
                   "score for each algorithm\n")
    try:
        choice_int = int(choice)
        if choice_int < 1 or choice_int > 3:
            print('Incorrect number entered. Try again.')
            continue
        else:
            break
    except ValueError:
        print('Invalid input. Enter either a 1, 2 or 3 depending on what you would like to do.')
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
        number = input("Enter an article (1) or summarise from file (2)?\n")
        try:
            file_or_keyboard = int(number)
            if num_of_sentences < 1:
                print("Invalid input, pick either 1 or 2.")
                continue
            elif num_of_sentences > 2:
                print("Invalid input, pick either 1 or 2.")
                continue
            break
        except ValueError:
            print("Invalid input, pick either 1 or 2.")
    if file_or_keyboard == 1:
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
    elif file_or_keyboard == 2:
        print("Enter the location of the file\n")
        file = input()
        count_file = open(file, "rt")
        data = count_file.read()
        total_word_count = data.split()
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
    tweets = client.search_tweets(keywords=tweet_topic, limit=50, lang='en')

    tweetSummarizer = TweetSummarizer()

    # clean tweets and store in tweets.csv
    rows = []
    for tweet in tweets:
        # print(tweet['text'])
        rows.append(str(tweet['text']).encode('utf-8', 'ignore'))
    if len(rows) > 0:
        for i in range(0, len(rows)):
            rows[i] = clean_tweet(rows[i])
        with open('tweets.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter='\n')
            writer.writerow(rows)

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
    print('TextRank ROUGE 1 scores:', rouge_1_scores[0])
    print('LexRank ROUGE 1 scores:', rouge_1_scores[1])
    print('LSA ROUGE 1 scores:', rouge_1_scores[2])
    print('KL-Sum ROUGE 1 scores:', rouge_1_scores[3])
    print('Luhn ROUGE 1 scores:', rouge_1_scores[4])
    print('SumBasic ROUGE 1 scores:', rouge_1_scores[5])

# have word count, percentage and time at top and then display each beneath so they are aligned
# for testing record times and put in graph to ensure timing are correct
