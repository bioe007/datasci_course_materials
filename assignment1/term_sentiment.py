# Perry Hargrave
#
# For Introduction to Data Science on Coursera
#
# NOTE: I don't give a crap about good looking code here
#
# Basic order of operations/stream of conciousness here...
# 1. Read tweets from file, linewise
# 2. Find each tweet's text
#      "lol, i'm solid - accept my greatness"
# 3. data cleanup - lowercase, remove punctuation
#      "lol im solid accept that i am the greatest"
#
# Option A.
# 4. Compute the sentiment score based on AFINN.txt
# 5. +1 for a positive message, -1 for a negative message
#
# Option B.
#
# 4. Replace each term present in sentiment file with the word's sentiment score
#      "3 im 2 1 that i am the 3" ==> 3+2+1+3 = 9
#
# 4. Average the words nearest neighbors sentiments
#       im = 3+2/2 = 2.5
#       that = 1 + 0/ 2  = 0.5
#       i = 0
#       am = 0
#       the = 3
#   * What about articles? Those really shouldn't be scored.
#
# Option C.
# 4. Compute tweet sentiment based on AFINN.txt
# 5. Score new words as average of tweet sentiments we get:
#      word_score = (sentiment[0] + sentiment[k-1] + sentiment[k])/k
#

from collections import OrderedDict
import csv
import json
import os
import pickle
import sys

SENTIMENT_FILENAME = "AFINN-111.txt"
TWEET_FILENAME = "./output.txt"


class TermDict(dict):
    """Custom dictionary to always make zeros and update by adding.

    All the sentiment values are forced to floats when 'update' is called.
    """
    def __init__(self, *args):
        super(TermDict, self).__init__(*args)

    def update(self, *args, **kwargs):
        """Adds the values found to existing keys and averages them.

        """
        try:
            for k, v in args[0].iteritems():
                if self.has_key(k):
                    self[k] += v
                else:
                    self[k] = float(v)
        except AttributeError:
            print 'attr error'
            pass

        iter_keys = set(*args).intersection(kwargs)

        for k in iter_keys:
            if self.has_key(k):
                self[k] += kwargs[k]
            else:
                self[k] = kwargs[k]

    @staticmethod
    def fromkeys(S, v=0):
        return super(TermDict, TermDict).fromkeys(S, v)


##### Setup area
def load_sentiment(path_sentiment=SENTIMENT_FILENAME):
    """Returns an ordered dictionary loaded with sentiment file.

    Expects file formatted like:
        <word>\t<integer>

    Integers may be negative.
    """
    d_sentiment = OrderedDict()
    with open(path_sentiment, 'r') as tabfile:
        reader = csv.reader(tabfile, delimiter='\t')
        for row in reader:
            d_sentiment[row[0]] = int(row[1])
    return d_sentiment

def load_tweets(path_tweets=TWEET_FILENAME):
    """Loads json formatted text file of tweets and returns as a list.
    """
    tweet_data = []
    with open(path_tweets, 'r') as tf:
        for line in tf:
            try:
                tweet_data.append(json.loads(line))
            except ValueError, e:
                print("JSON parse error at {0}".format(tf.tell()))
                print(line)
    return tweet_data

def score_tweets(tweet_data, d_sentiment):
    """Score all tweets and non-sentiment words.

    tweet_data Tweets as converted from json.loads
    d_sentiment A dictionary based on AFINN.txt data

    Returns TermDict of the non-AFINN (new) words and their scores.
    """
    td_words = TermDict()
    for tweet in tweet_data:
        try:
            tweet_text = tweet['text'].lower()
        except KeyError:
            # It seems lots of activity like deletes and favorites are also
            # captured from the twitter api as I'm using it, so for now I just
            # ignore these 'non-tweet' actions.
            continue

        # Scoring work
        tw_words = set(tweet_text.split())
        tw_keys = tw_words.intersection(d_sentiment)
        tw_sent_value = sum([d_sentiment[k] for k in tw_keys])
        td_words.update({word:tw_sent_value for
                        word in tw_words.difference(tw_keys)})
        if abs(tw_sent_value) >= 10:
            tweet['rager'] = True
            print('tweet: {0} score: {1}\n{2}'.format(tweet['id'],
                                                      tw_sent_value,
                                                    tweet_text.encode('utf-8')))
    return td_words

def print_word_sentiment(word):
    """Shows term and sentiment computed for it.

    `word` A term _not_ included in the AFINN-111.txt file.

    Outputs to stdout a line formatted:
        <term> <sentiment score>\n
    """
    print("{0} {1}".format(word[0].encode('utf-8'), word[1]))

def main():
    sentiment = load_sentiment()
    tweets = load_tweets()
    new_words = score_tweets(tweets, sentiment)
    for word, value in new_words.iteritems():
        print_word_sentiment((word, value))

if __name__ == '__main__':
    main()
