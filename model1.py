import math
import tweepy

"""
Assigns an influence score to a user. The score is an integer from 0 to 100,
where 0 corresponds to no influence and 100 is the highest possible degree of
influence a user can exert on Twitter. Influence is assessed based on a user's
reach, credibility and the size of their audience.
"""

debugging=False

listThreshold = 25 #a "moderate" number to be listed at
followThreshold = 40 #a "moderate" follower ratio
reactionThreshold = 400
followersLowThreshold = 2000
followersHighThreshold = 1000*200

#must sum to 10
listWeight = 1
followRatioWeight = 2
reactionWeight = 1
verifiedWeight = 1
followersLowWeight = 3
followersHighWeight = 2

def auth():
    consumer_key = "1ceDRUwTN3nRchujEbjppcukV";
    secret_key = "JneAHLQmumCCCMKDocoMCnPDEP88SdmgrjaWZ70Y8FwPbOEBQj";
    combined_keys = consumer_key + ":" + secret_key;
    encoded_key = "Basic " + base64.b64encode(combined_keys);

    post_headers = {'authorization': encoded_key, 'content-type': 'application/x-www-form-urlencoded;charset=UTF-8'};
    post_data = {'grant_type': 'client_credentials'};
    pr = requests.post("https://api.twitter.com/oauth2/token", headers=post_headers, data=post_data);
    data = json.loads(pr.content)
    get_authorization = "Bearer " + data.get("access_token");
    return get_authorization

def __score (value, weight, threshold):
    try:
        return weight*(1-1/math.exp(value/threshold))
    except OverflowError:
        return weight
    

def getScore(listedCount,numFollowers,following,tweetReactions,isVerified):
    if(following==0):
        following = 1
    followRatio = numFollowers/following
        
    listScore = __score(listedCount, listWeight, listThreshold)
    followRatioScore = __score(int(followRatio), followRatioWeight, followThreshold)
    reactionScore = __score(tweetReactions, reactionWeight, reactionThreshold)
    followersLowScore = __score(numFollowers,followersLowWeight,followersLowThreshold)
    followersHighScore = __score(numFollowers,followersHighWeight,followersHighThreshold)
    
    if debugging:
        print(listScore/listWeight)
        print(followRatioScore/followRatioWeight)
        print(reactionScore/reactionWeight)
        print(followersLowScore/followersLowWeight)
        print(followersHighScore/followersHighWeight)
        print(isVerified/verifiedWeight)
    
    influenceScore = verifiedWeight*isVerified + listScore + followRatioScore + reactionScore + followersLowScore + followersHighScore
    return influenceScore

def userScore(theId):
    #get listed count
    #payload = {'q': hashtag, 'result_type': 'popular', 'count': 10}
    #get_headers = {'authorization': auth}
    #r = requests.get('https://api.twitter.com/1.1/search/tweets.json?', headers=get_headers, params=payload)
    auth = tweepy.OAuthHandler("1ceDRUwTN3nRchujEbjppcukV", "JneAHLQmumCCCMKDocoMCnPDEP88SdmgrjaWZ70Y8FwPbOEBQj")
    auth.set_access_token("724834639-vS22k2Eo2uLuGZjzPXqhzO3qGWFKbAYBuvvD98VX", "KlyEDP8fnB0SiQWI2FFr0iu5jm7cVfncpJhavPekKM2Wa")
    api = tweepy.API(auth)
    userId = []
    userId.append(theId)
    user = api.lookup_users(userId)
    for u in user:
        followers = u.followers_count
        listedCount = u.listed_count

        friends = u.friends_count
        lastTweetReactions = 0
        verified = u.verified
        if (u.statuses_count > 1 and not (u.protected)):
            try:
                lastTweetReactions = u.status.favorite_count + u.status.retweet_count
            except:
                lastTweetReactions = 0
        influenceScore = getScore(listedCount,followers,friends,lastTweetReactions,verified)
        return influenceScore











