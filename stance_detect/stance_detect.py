from tqdm import tqdm

# Local Imports
from utils import read_twitter_dataset, filter_dataset, str2list

from feature_extraction.feat_extract import FeatureExtraction



if __name__ == "__main__":
    num_users = 100
    min_tweets = 10
    # PRE PROCESSING
    # Get twitter dataset with specific features

    dataset_path = "./datasets/twitter_covid.csv"
    features_to_get = ["user_id", "username", "tweet", "mentions", "hashtags"]
    random_sample_size = 0
    dataset = read_twitter_dataset(dataset_path, features_to_get, random_sample_size, 10000)

    # Column names in dataset
    user_col = "user_id"
    hashtags_col = "hashtags"
    mentions_col = "mentions"
    tweets_col = "tweet"

    # GATHERING DATA FOR FEATURE EXTRACTION
    users_list = []
    hashtags_list = []
    mentions_list = []
    tweets_list = []

    for row in tqdm(dataset, desc="parsing rows"):
        users_list.append(row[user_col])
        hashtags_list.append(str2list(row[hashtags_col]))
        mentions_list.append( str2list(row[mentions_col]) )
        tweets_list.append(row[tweets_col])


    # Filter all users for top user, with atleast min tweets
    users_to_keep = filter_dataset(users_list, num_users= num_users, min_tweets=min_tweets)

    # Filtering rest of data, based on filtered users
    zipped = zip( users_list, hashtags_list, mentions_list, tweets_list )
    filtered_zipped = [ x for x in tqdm(zipped, desc="filtering") if x[0] in users_to_keep]
    users_list, hashtags_list, mentions_list, tweets_list = zip(* filtered_zipped)

    # FEATURE EXTRACTION
    ft_extract = FeatureExtraction()

    # hashtags feature vector
    hashtag_features = ft_extract.hashtags(users_list, hashtags_list)
    mention_features = ft_extract.mentions(users_list, mentions_list)
    tweet_features = ft_extract.tweets(users_list, tweets_list)
    
    