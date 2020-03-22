from datetime import datetime


class LongSummarizer:
    def __init__(self, name, type_of_summarizer):
        self.name = name
        self.time = 0
        self.type_of_summarizer = type_of_summarizer
        self.summary = ""
        self.num_of_words = 0
        self.percentage_reduction = 0

    def create_summary(self, parser, num_of_sentences, total_word_count):
        start_time = datetime.now()
        self.summary = self.type_of_summarizer(parser.document, num_of_sentences)
        end_time = datetime.now()
        self.time = end_time - start_time
        self.word_count(total_word_count)

    def display_summary(self):
        print("\n", self.name, ":")
        for sentence in self.summary:
            print(sentence)

    def word_count(self, total_word_count):
        for sentence in self.summary:
            string_sentence = str(sentence)
            len_of_sentence = list(map(len, string_sentence.split()))
            self.num_of_words += len(len_of_sentence)
        self.percentage_reduction = (len(total_word_count) - self.num_of_words) / len(total_word_count) * 100

    def display_comparison(self):
        print("Summarised word count for", self.name, ":", self.num_of_words, "    Percentage Reduction:",
              round(self.percentage_reduction, 2), "%", "    Time Taken: ", self.time.microseconds, " microseconds")
