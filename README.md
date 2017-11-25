# 381_Project

TO DO:

1. Choose a hashtag
2. Search for all tweets based on that hashtag
3. Convert JSON data into dictionary, iterate through dictionary creating new dictionary where Key = User ID and Value = Tweet Id.
4. Iterate through dictionary, for each entry <K, V>
    1. create a node of the User ID, K
    2. GET request of retweets based on the Tweet ID, V
    3. For each User ID in the retweet results, create a node and connect an edge to the original user ID, K
    4. Make the weight the number of favorites the retweet received

There are other ways to go about doing this, this is just an idea for the algorithm.
