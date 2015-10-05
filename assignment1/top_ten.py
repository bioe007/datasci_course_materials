"""! @file  top_ten.py

   @brief

   @author  Perry Hargrave
   @date    2015-10-03

Print the top ten hashtags and their frequency (among all hashtags) from a
sample twitter stream data file. The tags should be printed:
    <hashtag> <frequency>

1. Count _unique_ hashtags
2. Calculate frequency of each unique hashtag
3. print hashtag and it's frequency to stdout

Twitter parses hashtags from each tweet's text as a _hashtag_ entity and so an
array of hashtags is accessible:
    'entities': {
        'hashtags' : [
            'text' : "<hashtag text>"
            indices: [ <indexes where tag was extracted from> ]
            ]
        }

It looks like the starting and ending indices are given in the list, so count
could be len(indices) / 2 ?
Still need to figure out what it does with multiple hashtags and re-use of the
same hashtag.
"""

from collections import Counter

from happiest_state import get_usa_tweets
import term_sentiment

class NoHashTags(Exception):
    pass

def get_tags(tw):
    tags = term_sentiment.TermDict()
    try:
        for d_tags in tw['entities']['hashtags']:
            tags.update({d_tags['text']:len(d_tags['indices'])/2})
    except KeyError:
        raise NoHashTags

    return tags

def print_some_tags(tweets):
    """a debugging/learning function"""
    for tw in tweets:
        try:
            print(get_tags(tw))
        except NoHashTags:
            continue

def compute_tag_freq(tweets):
    """Workhorse function, this solves the bulk of the problem.
    """
    tags = Counter()
    num_tags = 0
    for tw in tweets:
        try:
            new_tags = get_tags(tw)
        except NoHashTags:
            continue
        tags.update(new_tags)
        num_tags += sum(new_tags.itervalues())
    return tags, num_tags

if __name__ == "__main__":
    tweets = term_sentiment.load_tweets()
    hashtags, num_tags = compute_tag_freq(tweets)
    for tag in hashtags.most_common(10):
        print("{0} {1}".format(tag[0].encode('utf-8'), tag[1] / num_tags))

