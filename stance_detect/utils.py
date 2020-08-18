# Imports
from csv import DictReader
from tqdm import tqdm
from random import sample

## HELPER FUNCTIONS

# IMPLEMENT FUZZY STRING MATCHING
def get_tweet_counts(list_of_tweets, fuzzy_matching=False, fuzzy_matching_threshold=0.7):
    """Returns a list containing tuple((tweet): count), sorted by count in descending order.
    The first element (tweet) is a tuple, and may aggregate multiple tweets
    as one, based on the tweet_similarity function.
    Arguments:
        list_of_tweets (list)           : list of strings, where each string is a tweet.
        fuzzy_matching (bool)           : To find similar tweets using fuzzy string matching.
                                          Default: False.
        fuzzy_matching_threshold (int)  : Similarity threshold for fuzzy string matching over 
                                          which to consider two tweets similar.
                                          Default: 0.7.
    Returns:
        tweet_counts (list)             : List containing ((tweet/s), count).
    """
    if not fuzzy_matching:
        unique_tweets = set(list_of_tweets)
        tweet_counts = {tuple(tweet):list_of_tweets.count(tweet) for tweet in unique_tweets}
        tweet_counts =  sorted(tweet_counts.items(), key=lambda item: item[1], reverse=True)

    if fuzzy_matching:
        pass
        # TO BE IMPLEMENTED

    return tweet_counts


# List to Sorted counts dict
def sorted_count(array, reverse=True):
    """Returns a list containing tuple (value, count) of each unqiue value
       in the list, in desceding order.
    """
    sorted_count_list = {x:array.count(x) for x in set(array)}
    sorted_count_list =  sorted(sorted_count_list.items(), key=lambda item: item[1], reverse=reverse)
    return sorted_count_list


# String to List
def str2list(string):
    """Returns list contained in a string.
    Arguments:
        string (str)        : A string containing a list
    Returns:
        output (list)      : list of infered from the string
    """
    # Removing brackets "[" "]" from the string
    string = string[1:-1]

    # Splitting at ","
    output = string.split(",")

    # Removing trailing, leading space and residue ' ' characters
    output = [ string.strip()[1:-1] for string in output ]

    return output




# Get twitter dataset: uses Pythons native csv DictReader
def read_twitter_dataset(dataset_path="", features=[], random_sample_size=0, rows_to_read=None):
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
    with open(dataset_path, encoding="utf8") as csv_file:  
        dataset = DictReader(csv_file)
        for i,row in enumerate(tqdm(dataset, leave=True, desc="Reading rows")):
            if features:
                out = dict( (feat,row[feat]) for feat in features )
                output.append( out )
            else:
                output.append( row )
            
            if i==rows_to_read:
                break
    
    # Select random samples
    if random_sample_size:
        try:
            output = sample(output, random_sample_size)
        except:
            raise ValueError(f"random_sample_size larger than dataset size: {len(output)} or negative !")

    return output




# Filter Dataset for top users with tweets>min_tweets
def filter_dataset(users_list, num_users=100, min_tweets=10, user_col="user_id"):
    """Returns filtered dataset for users top users with tweets
       greater than or equal to min_tweets.

    Arguments:
        users_list (list)    : List of users to filter.
        num_users (int)      : Number of top users to cluster
        min_tweets (int): Min number of tweets to consider a user "active/engaged"
        user_col (str)       : Name of column containing user name or user id
    Returns:
        users_to_keep (list)  : list of users to keep.
    """
    print("Filtering rows")
    # Get sorted user counts
    user_counts = sorted_count(users_list)

    # Selecting top num_users
    user_counts = dict(user_counts[:num_users])

    # Selecting with greater than or equal to min_tweets
    user_counts = {k:v for k,v in user_counts.items() if v>= min_tweets}
    users_to_keep = set(user_counts.keys())

    return users_to_keep
