"""frequency.py

    author  Perry Hargrave
    date    2015-10-01

Problem statement:
    compute the term frequency histogram of data from problem 1.

    freq. term = [#term in all tweets] / [# all terms in all tweets]

    The denominator seems equivalent to "count all words."

    > python frequency.py <tweet_file>
    <term:string> <term_frequency:float>


PLAN:
    1. Read the tweets
    2. Split each tweet into a dict
        k = term, v = # of repeats in that tweet
    3. Increment-update the master term_dict with dict from #2
        This is already done in term_sentiment.TermDict
"""

from collections import Counter

# OK, I'm sick of rewriting shit for each problem...
import term_sentiment


def get_tweet_text(tweet):
    """Grab the text of a tweet.
    """
    try:
        return tweet['text'].lower()
    except KeyError:
        # It seems lots of activity like deletes and favorites are also
        # captured from the twitter api as I'm using it, so for now I just
        # ignore these 'non-tweet' actions.
        return ''

def count_terms(tweet):
    """Count frequency of terms in a tweet.

    Return a dict of the words in a tweet and their number of occurrences.
    """
    tw_text = get_tweet_text(tweet)
    return Counter(tw_text.split())

if __name__ == "__main__":
    tweets = term_sentiment.load_tweets()

    # This will hold all the unique terms
    term_dict = term_sentiment.TermDict()

    for tweet in tweets:
        term_dict.update(count_terms(tweet))

    total_terms = sum(term_dict.itervalues())

    # TODO: Filter the non-word terms like urls and separate hash tags???
    for term, freq in term_dict.iteritems():
        if freq <= 5:
            continue

        try:
            #I'm being cheap and skipping non-western'ish looking text now.
            print("{0} {1:.3}".format(term, freq / total_terms))
        except UnicodeError:
            pass

    print("total terms = ", total_terms)
    print("lol=", term_dict['lol'] / total_terms)
    print("love=", term_dict['love']/ total_terms)
    print("hate=", term_dict['hate']/ total_terms)
    print("happy=", term_dict['happy']/ total_terms)
