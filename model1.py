import math
import tweepy
from itertools import cycle

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
    key = 2  
    CONSUMER_KEY       =     [
            #'9XkYgKXCTL6KH0JOws7pkKszG',
            'jwOVv0V5uVdpXTtP5M6DyJv6C',
            'FnBA0hwuwZIhDR1qw0XQFrkla',
            'CZHFL5vpmTdQomW4vIkN9YFx3',
            '869B1o1dObkOCUa6mYK39wLtr',
            'lCUP345500lBRfEHUFFJSnfHC',
            'IaNc49MSj4BFQCE5txsZGO38C',
            '5Q53ZAFMikFU9qSGeEGhWFMCK',
            'zU5cVXdYWyLRpHWnw4HJ2nMEH',
            'STYydh05pVfg8g3sk3WPl3olO',
            'WQW8XQfgsyMhYprMLhbLDNUMs',
            'UaGCGoELlrcyDdyvBti5Ej35a',
            'ijWJksuc5EUEnVFMQZgwHGxr9',
            'csrsm9PcnevSPxSKHGk0fRDyM',
            'Uca7hOrDp0cDkITmbz9M0rE8N',
            'mTzztjybcdDiMROkP8WTV6viy',
            'FXbfn41cvtaSf7lqit497360j',
            'mp0MhtO7xdavD1JDZfGrMSkkH',
            'YP3TpcyqDIGTcaaQ6oCjHSeSy',
            '30TQMX9tqDIoWhepFio2p7MEV'
            ]
    CONSUMER_SECRET    =     [
            #'7wdo3HpkOlvS9cfxoAqmRKOuyJcAyx9EEuARBRzFKnfX3yhDL5',
            'mEI4IFTj31LmePCNUElz4BxV0fNch069pa5c4t8iNe8jYOsfoL',
            '0slkgdEH3istWudTcfX1BlucCqVBikHmGycjdfmCFO0fm44Rqe',
            'jScXxI48mvhjsl5wKCrIr1Ie1ay6MKMUVR77xYZdZONHZFCgrE',
            'kM5lG4QmKo7adftZH5P54WBojC1ZjffKXuNoeGm3GG99TDmZ1Q',
            'NVrvIMy4F4AyfvzUEpjqQRwYAt4lCr8uZmPzpmQYYixr1Oy4MC',
            'Mo5LuQlyyxuVM3sb1qqCsvXrKS6DYhNcI09L4tJ4QA1KLfXsRf',
            'DObc6k8QgRitM5K3FUeIbrpe0Us0QaUKXJNkXlySGxCfxxWbRs',
            'GjksjXC3wzf8KwVKlPf61V2h17Bz3enxym14aQs1KypIpefmXH',
            'wk4EYd7apTq9EHOZQBGoMGoNGariT19TLcbsGQEv0q3QVwFbIi',
            'J8vmE6TSkcnCS79WAzXfdAYYucmauEWJrHkDe0bjGTAWuuSX0F',
            'xvdpylM5KSdrZQGV3lDV2yDoo9jQ5qthNXuZBrjXYwrMn0MxNj',
            'wOgeyd52T2jWJJMfXGtaO28CCUEgGhaQmqbsMsDVHFva6I9tCT',
            '6goPwIaqbRPwZYA3Dcyarffid1guhiTT9czgRSuBa3u28ImBXF',
            'mGi9bncEv47X4NYrOsXQTNsaVoBwTtD6K8Z8sGbtcqwk9nE6kT',
            '2NawKGXMrh5XyGeVAFSyTILhEQiKAx2788xF8txuSzsqVbJw21',
            't8cdQu8o58I8y7nQfEtwMPLzDw8uyeSY8xadTLfbPxeRlOtRxY',
            'TwNdLCVU30Z3ygnsqlu7GWf9QPFcv7M0vyssOTJCM69I7mF6Jz',
            'BsyrHg8SKHqOaALhltqn7HJraL5iIF3faWoVbaAe1Vwxnw76M0',
            'hqyOjHI6d0j2G1yCLpwR6FnQYGYl7Scldq8sRsxv9BcygPK6q7'
            ]   
    OAUTH_TOKEN        =     [  
            #'745277343736995844-rRDSeonuJbi56e9QkgNpTxLLIJ6zaym',
            '745277343736995844-RYCMDprABDve3CqY2hkCOZOTuWzOcS3',
            '745277343736995844-fsBMNygESaLKxbJbZvhE49l7CoUfUv6',
            '320947567-H5rRzPhUdRIkO7MYeuYxU3pZ0EP8MUJICHHWUM2e',
            '320947567-yLoWHmhe5Dqr3GKNh6hq9raiwgSf6EFWClwPZTCU',
            '320947567-21vMgnoRjemCLYrYlUUvBf8gSyvxzk96uNkSxXqa',
            '743126394432040960-ZNxyQOQvM1MLkzakYL3Nfgo35NP9rMJ',
            '198256534-mJtqR6btkKF5x8YCpMgFhFokZU8abS7hTsy2j4bP',
            '198256534-3FUL51zQtHZnFevGcpTOdgwG8VrB5s4VlG3cwQpC',
            '198256534-UQxRP9D8UZiAlHKOnT3Hf6sEMKwWJet8T8qm9SBD',
            '743465390915919872-HEGyRJfayv3x2dNhN1LnpGB9tIM69NR',
            '743465390915919872-3BJxG7xzpGOaBydnMDNB9LSSNVIOqWc',
            '743465390915919872-Jjt7US7vRdvMhzC1tz8cAIUVAx0z7WG',
            '743465390915919872-mgU0Ju8IiEqO88XJa3XEF2J9oDjEHy3',
            '743465390915919872-lLfJQlzNbLZ67AmtX3B05QRCUASt7Ko',
            '743465390915919872-xXb3wi8vpxPvOPUNxCMLAZdT4n2JIe7',
            '1176891456-f1MgVmWZASgXv3cbEul1E0yvlNxmUddhFUB24PO',
           '1176891456-R4IdAaYGNJ9VnxPBSVfZgl8Ul3A4luHxJiPYOKx',
           '1176891456-gY9ipJFmZgsYrYfZWVocOTLfq7wTJ5PzoNtAGRs',
           '1176891456-3ZNiISR9zrMwMx4bqwEss1SlSDfpAsUaNPjcAki'
            ]
    OAUTH_TOKEN_SECRET =     [      
            #'XlkXHOLAiY7bFUVImAq1qr8qzeWugd5ihbnpnmnlYVMwx',
            'QHOVrvfpki9yj5sZF5x4w4iiQxzKPqZffMvqKGn8CUl6P',
            'AdyGaihD0UAmDIgrsMrtK8ZT0MSgaiPIIDlk8FBI4sFMX',
            'gCKK2e7eLGYUmRK7Wuczxge0NtpFLbvsRDjp6pNvKd15i',
            'A6oSCiCK5ykUfq27V6Fe3EkDTgoJyWiZxBWOGOpkrj7vQ',
            'JEE8Lj8l9nsYibbR73ienudwHo9jdcTdEahQQ8eeMyNIQ',
            'cyKMFUPwDbLj1Ew8pVK1tIpEXOpOwfH8KRtkJxPWTVKHO',
            'oN23zFXNCR73po9VdXNONsfpojNZem9F9poI5OBtVXpTL',
            'TU7Hj0tJ3qmLSVTWZGmuFE8eNCWQvxp7R4R0Rchskc5U5',
            'TSTdQC83ozbTfmmrD4uxBtm8bRHR3ILUgbVIlRNAKOkMY',
            'AfYFtkmAFM9dSpwPyVGB8Xy4ONDorEXcmDku8hu6szHMX',
            'Et6wuHdOJ6irUd9E1tstn5qoltm3HiwgxI8R2SnHPHhaw',
            'bCJELSuI40EPFlevcbEVZ9Pac8Ir0PRfT1CdnX8NcoUdS',
            'Wq9Xht0usAMfLyOoToNFcF3RZFsCtHb13m2r4UDVoiYNT',
            'yZV2TBWwHLPVVtrU917HAznaOW2xpsTLIbFcviMHRCd8N',
            'smhjUJ8wgkyHGKy1Ur0Fj0j4Rk3ximhV4yelghtbhwypv',
            'uwaPy4d9TsIPMFrwjhzryW0N8iWTNbLLsH2T5XfdUo2Uc',
            'nPiyH2jPwFQPJS9LVj85LduI7cW83IblfoDskjjlFRvdZ',
            'yTrMYcxMA0pznOFkeIa3pQMtjH5ItLksUeLNbtOnW58Pw',
            'ucfcrrZhBYjosJ46T0XNliox1zGNlws8gT5g9e54MfKzf'
            ]
    sets = len(CONSUMER_KEY)
    key_cycle = cycle(range(0,sets)) 
    Set=[CONSUMER_KEY,CONSUMER_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET]
    auth = tweepy.OAuthHandler(CONSUMER_KEY[key], CONSUMER_SECRET[key])
    auth.set_access_token(OAUTH_TOKEN[key],OAUTH_TOKEN_SECRET[key])
    api = tweepy.API(auth)
    #limit = api.rate_limit_status()
    #limit_remaining = limit['resources']['users']['/users/lookup']['remaining']
    #print('Key: ', key, 'Requests Remaining: ', limit_remaining )
    # Go to first key that has calls left
    #while(limit_remaining == 0):      
    #   key = next(key_cycle)
    #   print("###LIMIT REACHED, SWITCHING KEYS###")
    #   print('###USING KEY SET #',key)
    #   auth = tweepy.OAuthHandler(CONSUMER_KEY[key], CONSUMER_SECRET[key])
    #   auth.set_access_token(OAUTH_TOKEN[key],OAUTH_TOKEN_SECRET[key])
    #   api = tweepy.API(auth)
    #   limit = api.rate_limit_status()
    #   limit_remaining = limit['resources']['users']['/users/lookup']['remaining']
    #auth = tweepy.OAuthHandler("1ceDRUwTN3nRchujEbjppcukV", "JneAHLQmumCCCMKDocoMCnPDEP88SdmgrjaWZ70Y8FwPbOEBQj")
    #auth.set_access_token("724834639-vS22k2Eo2uLuGZjzPXqhzO3qGWFKbAYBuvvD98VX", "KlyEDP8fnB0SiQWI2FFr0iu5jm7cVfncpJhavPekKM2Wa")
    try:
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
    except tweepy.TweepError as e:
            print("###Rate Limit Exceeded###")
            #check first key
            if (key == (sets - 1)):
             print("key thing")
             auth = tweepy.OAuthHandler(Set[0][0],Set[1][0])
             auth.set_access_token(Set[2][0],Set[3][0])
             api = tweepy.API(auth) 
             limit_remaining = limit['resources']['users']['/users/lookup']['remaining']
             if (limit_remaining != 180):
                print("Sleeping for secs")
                time.sleep(30)
            #key = next(key_cycle)   
            key = key + 1   
            print("###LIMIT REACHED, SWITCHING KEYS###")
            print('###USING KEY SET #',key)
            auth = tweepy.OAuthHandler(Set[0][key],Set[1][key])
            auth.set_access_token(Set[2][key],Set[3][key])
            try:
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
            except tweepy.TweepError as e:
                print("###Rate Limit Exceeded###")
                #check first key
                if (key == (sets - 1)):
                 print("key thing")
                 auth = tweepy.OAuthHandler(Set[0][0],Set[1][0])
                 auth.set_access_token(Set[2][0],Set[3][0])
                 api = tweepy.API(auth) 
                 limit_remaining = limit['resources']['users']['/users/lookup']['remaining']
                 if (limit_remaining != 180):
                    print("Sleeping for secs")
                    time.sleep(30)
                #key = next(key_cycle)   
                key = key + 1   
                print("###LIMIT REACHED, SWITCHING KEYS###")
                print('###USING KEY SET #',key)
                auth = tweepy.OAuthHandler(Set[0][key],Set[1][key])
                auth.set_access_token(Set[2][key],Set[3][key])

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


                #limit = api.rate_limit_status()
