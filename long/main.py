from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from long import LongSummarizer


def store_text(t):
    f = open("test.txt", "w")
    for item in t:
        f.write(item)
    f.close()


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

# have word count, percentage and time at top and then display each beneath so they are aligned
# for testing record times and put in graph to ensure timing are correct
