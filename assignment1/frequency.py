import sys
import json
import codecs
import re

def frequency(term, tweets):
    return sum((tweet.count(term) for tweet in tweets))

def main():
    en_words_rexp = re.compile(r"[\w']*")
    tweet_file = codecs.open(sys.argv[1], "r", "utf8")
    tweets = (json.loads(l).get(u"text", '').lower() for l in tweet_file)
    # tokenize:
    tweets = [en_words_rexp.findall(t) for t in tweets]
    all_terms = set().union(*tweets)
    all_terms.discard('')

    all_term_occurrences = sum((len(tweet) for tweet in tweets))
    term_frequency = {term: frequency(term, tweets) for term in all_terms if term}
    for term in all_terms:
        if term:
            print u"%s %0.3f" % (
                    term, float(frequency(term, tweets)) / all_term_occurrences)


if __name__ == '__main__':
    main()
