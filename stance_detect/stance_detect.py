# Local Imports
from utils import read_twitter_dataset




if __name__ == "__main__":

    # Get twitter dataset with specific features
    dataset_path = "./datasets/twitter_covid.csv"
    features_to_get = ["username", "tweet", "mentions", "hashtags"]
    random_sample_size = 0
    dataset = read_twitter_dataset(dataset_path, features_to_get, random_sample_size)

    # Filter Dataset
    
    MIN_USER_TWEETS = 10

    # 
    NUM_USERS_TO_CLUSTER = 100

    # dataset = 

    print(dataset[0])