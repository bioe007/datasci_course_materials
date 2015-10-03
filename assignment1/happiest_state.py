# -*- coding: utf-8
"""happiest_state.py

    author  Perry Hargrave
    date    2015-10-03

"""

import operator

from states import ABBREVIATION, FULLNAME
import term_sentiment

class SummingDict(dict):
    """Just sums values instead of setting them when 'update' is called.
    """
    pass
    def __init__(self, *args, **kwargs):
        super(SummingDict, self).__init__(self, *args, **kwargs)

    def update(self, *args, **kwargs):
        """Adds the values found to existing keys when found.
        """
        try:
            for k, v in args[0].iteritems():
                if self.has_key(k):
                    self[k] += v
                else:
                    self[k] = v
        except AttributeError:
            # The dict is unpopulated.
            pass

        iter_keys = set(*args).intersection(kwargs)

        for k in iter_keys:
            if self.has_key(k):
                self[k] += kwargs[k]
            else:
                self[k] = kwargs[k]



def show_location_verbose(tweet):
    try:
        loc_string = "id={0}".format(tweet['id'])
        if tweet['place'] is not None:
            loc_string += "\nplace={0}".format(tweet['place'])
        if tweet['coordinates'] is not None:
            loc_string += "\ncoord={0}".format(tweet['coordinates'])
    except KeyError:
        return None

    return loc_string


USA = "United States"

def check_country(tweet, country):
    try:
        if tweet['place']['country'] != USA:
            return False

        return True
    except (TypeError, KeyError):
        return False

def get_usa_tweets(tweets):
    """Checks tweet's country field matches `USA` string.
    """
    usa_tweets = [tw for tw in tweets if check_country(tw, USA) == True]
    return usa_tweets

def parse_state_by_city(tweet_place):
    """In city-type locations the last two chars are the state abbreviation.
    """
    k = tweet_place['full_name'][-2:].upper()
    if ABBREVIATION.has_key(k):
        return k
    else:
        print("{0} not found in ABBREV dict".format(k))
        raise KeyError

def get_state(tweet_place):
    """By convention, this will return the state's abbreviation.
    """
    if tweet_place['place_type'] == 'city':
        state_abbrev = parse_state_by_city(tweet_place)
    else:
        k = tweet_place['name']
        try:
            state_abbrev = FULLNAME[k]
        except KeyError, e:
            print("O shit..")
            print("tweet place", tweet_place)
            raise e

    return state_abbrev

def score_tweet(tweet_text, d_sentiment):
    tw_words = set(tweet_text.lower().split())
    tw_keys = tw_words.intersection(d_sentiment)
    tw_sent_value = sum([d_sentiment[k] for k in tw_keys])
    return tw_sent_value

if __name__ == "__main__":
    tweets = term_sentiment.load_tweets()
    sntmnt = term_sentiment.load_sentiment()

    usa_tweets = [tw for tw in tweets if check_country(tw, USA)]
    state_scores = dict.fromkeys(ABBREVIATION, 0)
    for tw in usa_tweets:
        state_scores[get_state(tw['place'])] += score_tweet(tw['text'], sntmnt)

    happy_value = max(state_scores.iteritems(), key=operator.itemgetter(1))
    # print "state={0} score={1}".format(happy_value[0], happy_value[1])
    print "state={0}".format(happy_value[0])


