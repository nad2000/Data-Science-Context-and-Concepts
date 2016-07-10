import sys
import json
import codecs
from itertools import groupby

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

states_rev = {name.lower(): code for (code, name) in states.items()}


def tweet_score(text, scores):
    if not text:
        return 0
    #return sum((scores.get(w.strip().lower(), 0) for w in text.split(' ')
    return sum((scores[t] if t in text else 0 for t in scores))


def tweet_state(tweet):

    state = None

    # tweet location:
    if tweet.get("place") and tweet.get("place").get("country_code") == "US":
        location = tweet.get("place").get("full_name")
        if location:
            location = [lp.strip() for lp in location.split(',')]
            city = location[0]
            if len(location) > 1:
                state = location[1].upper()
                if state not in states.keys():
                    state = states_rev.get(city.lower())
                    if state not in states.keys():
                        state = None
            else:
                state = states_rev.get(city.lower())
                if state not in states.keys():
                    state = None
    if state:
        return state

    # based on the user
    user = tweet.get("user")
    if user:
        location = user.get("location")
        if location:
            location = [lp.strip() for lp in location.split(',')]
            city = location[0]
            if len(location) > 1:
                state = location[1].upper()
                if state not in states.keys():
                    state = states_rev.get(city.lower())
                    if state not in states.keys():
                        state = None
            else:
                state = states_rev.get(city.lower())
                if state not in states.keys():
                    state = None
    return state


def main():
    sent_file = codecs.open(sys.argv[1], "r", "utf8")
    tweet_file = codecs.open(sys.argv[2], "r", "utf8")
    scores = dict(((term, int(score)) for (term, score) in (line.split('\t') for line in sent_file)))
    tweets = [(tweet_state(tweet), tweet_score(tweet, scores)) for tweet in (json.loads(line) for line in tweet_file) if tweet_state(tweet)]
    sentiment = sorted([(sum((score for _, score in g)), state) for state, g in groupby(sorted(tweets), key=lambda t: t[0])])
    # happiest state:
    print sentiment[-1][1]
        

if __name__ == '__main__':
    main()
