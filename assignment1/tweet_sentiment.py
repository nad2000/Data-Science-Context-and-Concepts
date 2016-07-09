import sys
import json
import codecs

def tweet_score(text, scores):
    if not text:
        return 0
    #return sum((scores.get(w.strip().lower(), 0) for w in text.split(' ')
    return sum((scores[t] if t in text else 0 for t in scores))

def main():
    sent_file = codecs.open(sys.argv[1], "r", "utf8")
    tweet_file = codecs.open(sys.argv[2], "r", "utf8")
    scores = dict(((term, int(score)) for (term, score) in (line.split('\t') for line in sent_file)))
    for line in tweet_file:
        tweet = json.loads(line)
        print tweet_score(tweet.get(u"text"), scores)
        

if __name__ == '__main__':
    main()
