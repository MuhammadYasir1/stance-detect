from tqdm import tqdm

# Local Imports
from data_loading.load_data import read_dataset
from feature_extraction.feat_extract import FeatureExtraction




if __name__ == "__main__":

    ##### DATA LOADING #####
    # Get dataset columns
    users_list, usernames_list, tweets_list, mentions_list, hashtags_list  =  read_dataset(
                        dataset_path="./datasets/twitter_covid.csv", 
                        features=["user_id", "username", "tweet", "mentions", "hashtags"], 
                        num_users=None,
                        min_tweets=0,
                        random_sample_size=0, 
                        rows_to_read=10,
                        user_col="user_id", 
                        str2list_cols=["mentions", "hashtags"])



    ##### FEATURE EXTRACTION #####
    # Define features to use for Dim Reduction and Clustering
    # CONSISTENT WITH THE PAPER
    # T : tweets feature vectors
    # R : mentions OR retweets feature vectors
    # H : hashtags feature vector
    # Feature vectors will be concatenated in order
    FEATURES_TO_USE = ["T","R","H"]

    ft_extract = FeatureExtraction()
    user_feature_dict = ft_extract.get_user_feature_vectors(
                            features_to_use=FEATURES_TO_USE,
                            users_list, #positional args
                            tweets_list, 
                            mentions_list, 
                            hashtags_list,
                            feature_size=None,
                            relative_freq=True
                            )
    
    
    ##### DIMENSIONALITY REDUCTION #####
    