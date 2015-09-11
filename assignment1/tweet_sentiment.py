# Perry Hargrave
#
# For Introduction to Data Science on Coursera
#
from collections import OrderedDict
import csv
import json
import os
import pickle
import sys

# Sentiment work
# 1. Create dictionary from sentiment file
#   keys = words, values = sentiment score
#           I think this can be done with csvreader directly
#           Maybe nice to make an ordered dict, save the file pkl
# This will get slow if loading a lot.
sentiment_filename = "AFINN-111.txt"

d_sentiment = OrderedDict()
with open(sentiment_filename, 'r') as tabfile:
    reader = csv.reader(tabfile, delimiter='\t')
    for row in reader:
        d_sentiment[row[0]] = int(row[1])

# Tweet work
# 1. Convert using json library -> json.loads()
tweet_filename = "./output.txt"
tweet_data = []

with open(tweet_filename, 'r') as tf:
    for line in tf:
        try:
            tweet_data.append(json.loads(line))
        except ValueError, e:
            print("JSON parse error at {0}".format(tf.tell()))
            print(line)

# Tweet work
# 2. Figure out what are tweets, drop the rest
# 2.1 each tweet has a 'text', other actions don't seem to
for tweet in tweet_data:
    try:
        tweet_text = tweet['text'].lower()
    except KeyError:
        continue

    # Scoring work
    tw_words = set(tweet_text.split())
    tw_keys = tw_words.intersection(d_sentiment)
    tw_sent_value = sum([d_sentiment[k] for k in tw_keys])
    if tw_sent_value > 0:
        print('tweet: ', tweet['id'], tweet['text'])
        print('score', tw_sent_value)



# Tweet work
# 3. sum sentiment scores for each tweets text

print("We have {0} tweets".format(len(tweet_data)))
sys.exit(0)






def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    hw()
    lines(sent_file)
    lines(tweet_file)

if __name__ == '__main__':
    main()
