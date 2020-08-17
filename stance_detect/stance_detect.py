from tqdm import tqdm

# Local Imports
from utils import read_twitter_dataset, filter_dataset, str2list

from feature_extraction.feat_extract import FeatureExtraction



if __name__ == "__main__":
    # PRE PROCESSING
    # Get twitter dataset with specific features

    dataset_path = "./datasets/twitter_covid.csv"
    features_to_get = ["user_id", "username", "tweet", "mentions", "hashtags"]
    random_sample_size = 0
    dataset = read_twitter_dataset(dataset_path, features_to_get, random_sample_size, 10000)

    # Filter Dataset for top user, with atleast min tweets
    dataset = filter_dataset(dataset, num_users= 10, min_tweets=10)

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
        print(row[tweets_col])
        break
        users_list.append(row[user_col])
        hashtags_list.append(str2list(row[hashtags_col]))
        mentions_list.append( str2list(row[mentions_col]) )
        tweets_list.append(str(row[tweets_col]))



    # FEATURE EXTRACTION
    ft_extract = FeatureExtraction()
    # Hashtags feat vector for each user
    hashtag_features = ft_extract.hashtags(users_list, hashtags_list)

    print(tweets_list[0])