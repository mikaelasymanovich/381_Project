import math

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