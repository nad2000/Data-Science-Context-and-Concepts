import sys
import json
import codecs
from collections import Counter

tags = Counter()

def main():
    tweet_file = codecs.open(sys.argv[1], "r", "utf8")
    for line in tweet_file:
        tweet = json.loads(line)
        entities = tweet.get("entities")
        if entities:
            hashtags = entities.get("hashtags")
            for tag in hashtags:
                tags[tag.get("text")] += 1
                
    for tag, count in tags.most_common(10):
        print "%s %d" % (tag, count)
        

if __name__ == '__main__':
    main()
