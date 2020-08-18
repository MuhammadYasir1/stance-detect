import sys
sys.path.append("..")

import numpy as np

from tqdm import tqdm
from utils import sorted_count, get_tweet_counts

# For "n" users with "min_tweets" in dataset, we find
# Hashtags
# Retweeted Accounts
# Unique Tweets


class FeatureExtraction():
    def __init__(self):
        return


    def hashtags(self, users_list, hashtags_list, feature_size=None, relative_freq=True):
        """Returns a list of dictionary, with hashtag features for each user.
        Arguments:
            users_list (list)           : List of all users in the dataset (Non-Unique).
            hashtags_list (list)        : List of list of all hashtags shared.
            feature_size (int)          : Length of the hashtags feature vector
                                          (Equivalent to selecting top popular hashtags)
                                          If None - uses all hashtags in the dataset.
            relative_freq (bool)        : Whether to compute feature vector with relative
                                          count i.e. divide by total count.
        Returns:
            hashtag_features (dict)     : Dictionary, with user_col as key and
                                           hashtag feature vector as value.
        """
        # get the counts of each hashtag shared
        # Collapse the list of lists: hashtags_list
        hashtag_counts = sorted_count([h for l in hashtags_list for h in l])

        # fitler against feature_size, Default is None=Selects all.
        hashtag_counts = hashtag_counts[:feature_size]
        hashtag_vector = [h for h,_ in hashtag_counts]

        # zip users,hastags
        users_hashtags = zip(users_list, hashtags_list)

        # findng hashtag feature for each user
        hashtag_features = {}
        for user in tqdm(set(users_list), desc="hashtag_features", leave=True):
            user_hashtags = [h for u,h in users_hashtags if u==user]
            hashtag_features[user] = np.array( [ user_hashtags.count(h) for h in hashtag_vector ] )
            if relative_freq and np.sum(hashtag_features[user])!=0:
                hashtag_features[user] = hashtag_features[user]/np.sum(hashtag_features[user])
        
        return hashtag_features
    

    def mentions(self, users_list, mentions_list, feature_size=None, relative_freq=True):
        """Returns a list of dictionary, with mentions features for each user.
        Arguments:
            users_list (list)           : List of all users in the dataset (Non-Unique).
            mentions_list (list)        : List of list of all mentions shared.
            feature_size (int)          : Length of the mentions feature vector
                                          (Equivalent to selecting top popular mentions)
                                          If None - uses all mentions in the dataset.
            relative_freq (bool)        : Whether to compute feature vector with relative
                                          count i.e. divide by total count.
        Returns:
            mention_features (dict)     : Dictionary, with user_col as key and
                                           mention feature vector as value.
        """
        # Collapsing mentions of users into a single list
        all_mentions = [x for m in mentions_list for x in m if x]
        mention_counts = sorted_count(all_mentions)

        mentions_vector = [m for m,_ in mention_counts]

        # zip users, mentions
        users_mentions = zip(users_list, mentions_list)
        # findng mention feature vector for each user
        mention_features = {}
        for user in tqdm(set(users_list), desc="mention_features", leave=True):
            user_mentions = [m for u,m in users_mentions if u==user]
            mention_features[user] = np.array( [ user_mentions.count(m) for m in mentions_vector ] )
            if relative_freq and np.sum(mention_features[user])!=0:
                mention_features[user] = mention_features[user]/np.sum(mention_features[user])
        
        return mention_features


    def tweets(self, users_list, tweets_list, feature_size=None, relative_freq=True):
        """Returns a list of dictionary, with tweets features for each user.
        Arguments:
            users_list (list)           : List of all users in the dataset (Non-Unique).
            tweets_list (list)          : List of list of all tweets shared.
            feature_size (int)          : Length of the tweets feature vector
                                          (Equivalent to selecting top popular tweets)
                                          If None - uses all tweets in the dataset.
            relative_freq (bool)        : Whether to compute feature vector with relative
                                          count i.e. divide by total count.
        Returns:
            tweet_features (dict)       : Dictionary, with user_col as key and
                                           tweet feature vector as value.
        """
        # Get tweet counts, sorted by count in descending order
        tweet_counts = get_tweet_counts(tweets_list, fuzzy_matching=False)

        # Tweet Vector
        tweets_vector = [tweet for tweet,_ in tweet_counts]

        # zip users, tweets
        users_tweets_zip = zip(users_list, tweets_list)

        # findng tweet feature vector for each user
        tweet_features = {}
        for user in tqdm(set(users_list), desc="tweet_features", leave=True):
            user_tweets = [ tweet for u,tweet in users_tweets_zip if u==user ]
            tweet_features[user] = np.array( [ user_tweets.count(tweet) for tweet in tweets_vector ] )
            if relative_freq and np.sum(tweet_features[user])!=0:
                tweet_features[user] = tweet_features[user]/np.sum(tweet_features[user])
        
        return tweet_features