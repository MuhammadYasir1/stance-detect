# Imports
from csv import DictReader
from tqdm import tqdm
from random import sample


# Get twitter dataset
# Uses Pythons native csv DictReader
def read_twitter_dataset(dataset_path="", features=[], random_sample_size=0):
    """Return the csv twitter dataset in a dictionary.
    Arguments:
        dataset_path (str)      : Path to the dataset csv file
        features (list)         : List of feature/columns names to return
        random_sample_size (int): Number of random samples to select from the dataset
                                  must be less than the total dataset size
    Returns:
        dataset (list)      : list of csv rows as dictionaries
    """
    if not dataset_path:
        raise ValueError("Arguement dataset_path not defined !")

    output = []
    with open(dataset_path) as csv_file:  
        dataset = DictReader(csv_file)
        for row in tqdm(dataset, leave=False, desc="Reading rows"):
            if features:
                out = dict( (feat,row[feat]) for feat in features )
                output.append( out )
            else:
                output.append( row )
    
    # Select random samples
    if random_sample_size:
        try:
            output = sample(output, random_sample_size)
        except:
            raise ValueError(f"random_sample_size larger than dataset size: {len(output)} or negative !")

    return output



# Filter Dataset for top users with tweets>MIN_USER_TWEETS
def filter_dataset(num_users=100, min_user_tweets=10, user_col="username"):
    """Returns filtered dataset for users top users with tweets
       greater than or equal to min_user_tweets.

    Arguments:
        num_users (int)      : Number of top users to cluster
        min_user_tweets (int): Min number of tweets to consider a user "active/engaged"
        user_col (str)       : Name of column containing user name or user id
    Returns:
        dataset (list)      : list of filtered csv rows as dictionaries
    """
    #Get all users
    users = [row[user_col] for row in dataset]

    # Filtering users with greater than or equal to min_user_tweets
    output = [row for row in dataset if users.count(row[user_col])>=min_user_tweets ]



    return