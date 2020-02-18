from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from datetime import datetime
import rogue.

def display_summary(name, summarizer):
    print("")
    print(name, ":")
    for sentence in summarizer:
        print(sentence)


def store_text(t):
    f = open("test.txt", "w")
    for item in t:
        f.write(item)
    f.close()


def word_count(summary):
    num_of_words = 0
    for sentence in summary:
        string_sentence = str(sentence)
        len_of_sentence = list(map(len, string_sentence.split()))
        num_of_words += len(len_of_sentence)

    return num_of_words


def display_comparisons(name, num_of_words, percentage_reduction, time):
    print("Summarised word count for", name, ":", num_of_words, "    Percentage Reduction:",
          round(percentage_reduction, 2), "%", "    Time Taken: ", time, " microseconds")


num_of_sentences = input("How many sentences")
text = []
print("Enter text")
while True:
    try:
        line = input()
    except EOFError:
        break
    text.append(line)

store_text(text)
count_file = open("first.txt", "rt")
data = count_file.read()
total_word_count = data.split()
file = "first.txt"
parser = PlaintextParser.from_file(file, Tokenizer("english"))


textrank = TextRankSummarizer()
lexrank = LexRankSummarizer()
lsa = LsaSummarizer()
kl_sum = KLSummarizer()
luhn = LuhnSummarizer()
sumbasic = SumBasicSummarizer()

textrank_start_time = datetime.now()
textrank_summary = textrank(parser.document, num_of_sentences)
textrank_end_time = datetime.now()
textrank_time = textrank_end_time - textrank_start_time

lexrank_start_time = datetime.now()
lexrank_summary = lexrank(parser.document, num_of_sentences)
lexrank_end_time = datetime.now()
lexrank_time = lexrank_end_time - lexrank_start_time

lsa_start_time = datetime.now()
lsa_summary = lsa(parser.document, num_of_sentences)
lsa_end_time = datetime.now()
lsa_time = lsa_end_time - lsa_start_time

kl_sum_start_time = datetime.now()
kl_sum_summary = kl_sum(parser.document, num_of_sentences)
kl_sum_end_time = datetime.now()
kl_sum_time = kl_sum_end_time - kl_sum_start_time

luhn_start_time = datetime.now()
luhn_summary = luhn(parser.document, num_of_sentences)
luhn_end_time = datetime.now()
luhn_time = luhn_end_time - luhn_start_time

sumbasic_start_time = datetime.now()
sumbasic_summary = sumbasic(parser.document, num_of_sentences)
sumbasic_end_time = datetime.now()
sumbasic_time = sumbasic_end_time - sumbasic_start_time

display_summary("TextRank", textrank_summary)
display_summary("LexRank", lexrank_summary)
display_summary("LSA", lsa_summary)
display_summary("KL-Sum", kl_sum_summary)
display_summary("Luhn", luhn_summary)
display_summary("SumBasic", sumbasic_summary)

print("")
print("Total number of words: ", len(total_word_count))
display_comparisons("TextRank", word_count(textrank_summary), ((len(total_word_count) - word_count(textrank_summary)) /
                                                               len(total_word_count)) * 100, textrank_time.microseconds)
display_comparisons("LexRank", word_count(lexrank_summary), ((len(total_word_count) - word_count(lexrank_summary)) /
                                                             len(total_word_count)) * 100, lexrank_time.microseconds)
display_comparisons("LSA", word_count(lsa_summary), ((len(total_word_count) - word_count(lsa_summary)) /
                                                     len(total_word_count)) * 100, lsa_time.microseconds)
display_comparisons("KL-Sum", word_count(kl_sum_summary), ((len(total_word_count) - word_count(kl_sum_summary)) /
                                                           len(total_word_count)) * 100, kl_sum_time.microseconds)
display_comparisons("Luhn", word_count(luhn_summary), ((len(total_word_count) - word_count(luhn_summary)) /
                                                       len(total_word_count)) * 100, luhn_time.microseconds)
display_comparisons("SumBasic", word_count(sumbasic_summary), ((len(total_word_count) - word_count(sumbasic_summary)) /
                                                               len(total_word_count)) * 100, sumbasic_time.microseconds)

# have word count, percentage and time at top and then display each beneath so they are aligned


# system summary(predict) & reference summary
summary = [[" Tokyo is the one of the biggest city in the world."]]
reference = [[["The capital of Japan, Tokyo, is the center of Japanese economy."]]]

# initialize setting of ROUGE to eval ROUGE-1, 2, SU4
# if you evaluate ROUGE by sentence list as above, set summary_file_exist=False
# if recall_only=True, you can get recall scores of ROUGE
rouge = Pythonrouge(summary_file_exist=False,
                    summary=summary, reference=reference,
                    n_gram=2, ROUGE_SU4=True, ROUGE_L=False,
                    recall_only=True, stemming=True, stopwords=True,
                    word_level=True, length_limit=True, length=50,
                    use_cf=False, cf=95, scoring_formula='average',
                    resampling=True, samples=1000, favor=True, p=0.5)
score = rouge.calc_score()
print(score)
