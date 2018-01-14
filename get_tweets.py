import requests
import base64
import json
import networkx as nx
import matplotlib.pyplot as plt
import model1



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
		payload = {'q': hashtag, 'result_type': 'popular', 'count': 10}
		get_headers = {'authorization': auth}
		r = requests.get('https://api.twitter.com/1.1/search/tweets.json?', headers=get_headers, params=payload)
		parsed = json.loads(r.content)
		graph = make_graph(auth, parsed, graph)
	showGraph(graph)
	return graph


def make_graph(auth, tweets, G):
	user_tweet = {}
	users = []
	user_weights = {}
	max_weight = 0

	for tweet in tweets["statuses"]:
		user_id = tweet["user"]["id"]
		tweet_id = tweet["id_str"]
		user_tweet[user_id] = tweet_id
		users.append(user_id)
		weight_user = model1.userScore(user_id)

		if (user_id in user_weights):
			user_weights[user_id] = user_weights[user_id] + weight_user
			if (user_weights[user_id] > max_weight):
					max_weight = user_id
		else:
			user_weights[user_id] = weight_user
			if (user_weights[user_id] > max_weight):
					max_weight = user_id

		G.add_node(user_id, node_size=weight_user+ 0.1)
		payload1 = {'id': tweet_id}
		headers = {'authorization': auth}
		r = requests.get('https://api.twitter.com/1.1/statuses/retweeters/ids.json', headers=headers, params=payload1)
		retweeters = json.loads(r.content)
		print retweeters

		for retweeter in retweeters["ids"]:
			weight = model1.userScore(retweeter)
			#ADD 0.1 SO THE NODES OF SIZE 0.0 SHOW UP
			G.add_node(retweeter, node_size=weight+ 0.1)
			#print weight
			G.add_edge(retweeter, user_id, weight=weight) #change this weight accordingly

			if (retweeter in user_weights):
				print("yippee")
				user_weights[retweeter] = user_weights[retweeter] + weight
				if (user_weights[retweeter] > max_weight):
					max_weight = retweeter
			else:
				user_weights[retweeter] = weight
				if (user_weights[retweeter] > max_weight):
					max_weight = retweeter

	for key, value in sorted(user_weights.iteritems(), key=lambda (k,v): (v,k)):
   		print "%s: %s" % (key, value)
	print("max: ")
	print(max_weight)
	return G

def showGraph(graph):
	weights=nx.get_edge_attributes(graph,'weight')
	nx.draw(graph, node_color='#FF4500')
	pos = nx.spring_layout(graph)
	nx.draw_networkx_nodes(graph, pos,  node_color = '#FF4500')
	#nx.draw_networkx_labels(graph, pos)
	nx.draw_networkx_edge_labels(graph, pos, edge_color= '#000000', edge_labels=weights)
	#print(G.nodes)
	plt.show()

def main():
	G = nx.DiGraph()
	authorization = auth()
	#hashtags = ['#LilacFire', '#WeirdPlacestoSeeSanta', '#BeatTheHolidayBluesBy', '#StopTheFCC', '#EndWell17',
	#'#GenderEquityNYC', '#DontBeSurprisedWhen', '#NOvsATL', '#AllStars2017', '#CamilaWeAreYourRealFriends'] 
	hashtags = ['#FlyEaglesFly']
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


	gr = make_request(authorization, hashtags, G)




	#print hashtags




if  __name__ =='__main__':main()