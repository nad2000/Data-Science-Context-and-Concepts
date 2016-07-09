import sys
import json
import codecs
import re

def tweet_score(tweet, scores):
    if not tweet:
        return 0
    return sum((scores.get(w, 0) for w in tweet))

def find_score(term, tweets):
    return sum((tweet[1] for tweet in tweets if term in tweet[0]))

def main():
    en_words_rexp = re.compile(r"[\w']*")
    sent_file = codecs.open(sys.argv[1], "r", "utf8")
    tweet_file = codecs.open(sys.argv[2], "r", "utf8")
    scores = dict(((term, int(score)) for (term, score) in (line.split('\t') for line in sent_file)))
    tweets = [json.loads(l).get(u"text", '').lower() for l in tweet_file]
    # tokenize:
    tweets = [en_words_rexp.findall(t) for t in tweets]
    all_terms = set().union(*tweets)
    all_terms.discard('')

    unscored_terms = all_terms - set(scores.values())
    # add scores:
    tweets = [(t, tweet_score(t, scores)) for t in tweets]

    for term in all_terms:
        if term:
            print u"%s %0.3f" % (term, scores.get(term, find_score(term, tweets)))


if __name__ == '__main__':
    main()
