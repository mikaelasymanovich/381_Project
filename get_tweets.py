import requests
import base64
import json
import networkx as nx
import matplotlib.pyplot as plt
import model1
import model2
import numpy as np



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


def make_request(auth, hashtags, graph):
	for hashtag in hashtags:
		payload = {'q': hashtag, 'result_type': 'popular'}
		#payload = {'q': hashtag}
		get_headers = {'authorization': auth}
		r = requests.get('https://api.twitter.com/1.1/search/tweets.json?', headers=get_headers, params=payload)
		parsed = json.loads(r.content)
		make_graph(auth, parsed, graph)


def make_graph(auth, tweets, G):
	user_tweet = {}
	users = []
	user_weights = {}
	max_weight = 0
	originals = {}
	total_retweeters = []
	tweet_ids = []
	print("the total number of tweets are ", tweets["statuses"])
	for tweet in tweets["statuses"]:
		print("TWEET")
		user_id = tweet["user"]["id"]
		tweet_id = tweet["id_str"]
		if tweet_id in tweet_ids:
			continue
		else:
			tweet_ids.append(tweet_id)

		user_tweet[user_id] = tweet_id
		users.append(user_id)
		weight_user = model1.userScore(user_id)
		screen = get_screen_name(user_id, auth)

		if (user_id in user_weights):
			user_weights[screen] = user_weights[screen] + weight_user
			if (user_weights[screen] > max_weight):
					max_weight = user_id
		else:
			user_weights[screen] = weight_user
			if (user_weights[screen] > max_weight):
					max_weight = screen

		G.add_node(user_id, node_size=(weight_user *100 + 1))
		payload1 = {'id': tweet_id}
		headers = {'authorization': auth}
		r = requests.get('https://api.twitter.com/1.1/statuses/retweeters/ids.json', headers=headers, params=payload1)
		retweeters = json.loads(r.content)

		#print retweeters
		#print("ORIGINAL TWITTER USER: ", screen, " with retweeters ", retweeters["ids"])
		#print(originals)
		if not screen in originals:
			originals[screen] = []
			print("correct")
		else:
			print("wrong")

		for retweeter in retweeters["ids"]:
			if (not retweeter in originals[screen]):
				originals[screen].append(retweeter) #Adds Retweeter to list in dictionary
			if (not retweeter in total_retweeters):
				total_retweeters.append(retweeter) #Adds Retweeter to TOTAL list of retweeters

			weight = model1.userScore(retweeter)
			#ADD 0.1 SO THE NODES OF SIZE 0.0 SHOW UP
			G.add_node(retweeter, node_size=[weight * 100])
			#print weight
			G.add_edge(retweeter, user_id, weight=weight) #change this weight accordingly

			screen_name = get_screen_name(retweeter, auth)

			#HEREEEEEE
			if (retweeter in user_weights):
				user_weights[screen_name] = user_weights[retweeter] + weight
				if (user_weights[screen_name] > max_weight):
					max_weight = screen_name
			else:
				user_weights[screen_name] = weight
				if (user_weights[screen_name] > max_weight):
					max_weight = screen_name

	for key, value in sorted(user_weights.iteritems(), key=lambda (k,v): (v,k)):
   		print "%s: %s" % (key, value)
	print("max: ")
	print(max_weight)
	generate_matrix(originals, total_retweeters)
	showGraph(G, user_weights)

def showGraph(graph, user_weights):
	weights=nx.get_edge_attributes(graph,'weight')
	nx.draw(graph, node_color='#FF4500')
	pos = nx.spring_layout(graph)
	#nx.draw_networkx_nodes(graph, pos, node_color = '#FF4500')
	#nx.draw_networkx_edge_labels(graph, pos, edge_color= '#000000', edge_labels=weights)
	plt.show()

def get_screen_name(user, auth):

	payload = {'id': user, 'include_entities': 'false'}
	get_headers = {'authorization': auth}
	r = requests.get('https://api.twitter.com/1.1/users/show.json?', headers=get_headers, params=payload)
	parsed = json.loads(r.content)
	return(parsed.get('screen_name'))

def generate_matrix(og, retweeters):
	#retweeters = total retweeters
	print("original tweeters:", og)
	print("retweeters", retweeters)

	og_length = len(og) #Users who Tweeted (rows)

	#matrix = np.zeros((og_length,len(retweeters)))
	matrix = np.zeros((len(retweeters),len(retweeters)))
	print(og_length, "length retweeet ", len(retweeters))
	#For every row in the matrix
	count = 0
	for i in og:
		tweet_list = og[i] 
		N = len(og[i]) #number of people that retweeted that tweet
		for retweeter in tweet_list: # for each person that retweeted that tweet
			index = retweeters.index(retweeter) #get index in TOTAL list
			matrix[index][count] = 1.0/N
		count+=1
	print(matrix)
	page_rank(len(matrix), matrix)


	#If 0th entry in RT-list is in the list at the 0th index in dict, then set [0][0] to 1/N, etc.
def page_rank(N, matrix):
	Hhat = matrix
	pi = []
	N_row = []
	N_col = []

	for i in range(0, N):
		pi.append(1.0/N)
		N_row.append(1.0)
		N_col.append([1.0/N])

	theta = 0.85

	G_x = np.array(Hhat)*theta
	G_y = (1.0-theta)*np.array(N_row)*np.array(N_col)
	G = G_x + G_y

	#print(G)

	for i in range(0,40):
		pi = np.dot(np.transpose(pi), G)

	
	print ("pi: ", pi)


def main():
	G = nx.DiGraph()
	authorization = auth()
	#hashtags = ['#LilacFire', '#WeirdPlacestoSeeSanta', '#BeatTheHolidayBluesBy', '#StopTheFCC', '#EndWell17',
	#'#GenderEquityNYC', '#DontBeSurprisedWhen', '#NOvsATL', '#AllStars2017', '#CamilaWeAreYourRealFriends'] 
	hashtags = ['#MakeAmericaGreatAgain']
	#hashtags = ['#craylaAndGoodies']
	#'#BallondOr', '#CFBAwards', '#DraftingDemocracy', '#atxweather']
	#, '#ISEEC17']
	#, '#H\xe1blameBajito'] 
	#'#TLTechLive', '#FreeJah', '#SAClimateReady', '#AztecSchoolShooting', '#PolygonShow', '#TheFive'] #'#GoPackGo', '#ThursdayThoughts', '#PitMad', '#foodie'
	#US woeid: 23424977

	#get hashtags
	#payload = {'id': '23424977'}
	#header = {'authorization': authorization}
	#r = requests.get('https://api.twitter.com/1.1/trends/place.json', headers=header, params=payload)
	#hashtags_all = json.loads(r.content)[0]
	#for hashtag in hashtags_all["trends"]:
	#	if (hashtag["name"][0] == '#'):
	#		hashtags.append(hashtag["name"])


	make_request(authorization, hashtags, G)




	#print hashtags




if  __name__ =='__main__':main()