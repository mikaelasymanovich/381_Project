import requests
import base64
import json
import networkx as nx
import matplotlib.pyplot as plt

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
		payload = {'q': hashtag, 'result_type': 'popular', 'count': 100}
		get_headers = {'authorization': auth}
		r = requests.get('https://api.twitter.com/1.1/search/tweets.json?', headers=get_headers, params=payload)
		parsed = json.loads(r.content)
		graph = make_graph(auth, parsed, graph)
	showGraph(graph)


def make_graph(auth, tweets, G):
	user_tweet = {}
	users = []
	for tweet in tweets["statuses"]:
		user_id = tweet["user"]["id"]
		tweet_id = tweet["id_str"]
		user_tweet[user_id] = tweet_id
		users.append(user_id)
		G.add_node(user_id)
		payload1 = {'id': tweet_id}
		headers = {'authorization': auth}
		r = requests.get('https://api.twitter.com/1.1/statuses/retweeters/ids.json', headers=headers, params=payload1)
		retweeters = json.loads(r.content)
		for retweeter in retweeters["ids"]:
			G.add_node(retweeter)
			G.add_edge(user_id, retweeter)
	return G

def showGraph(graph):
	nx.draw(graph)
	plt.show()

def main():
	G = nx.Graph()
	authorization = auth()
	hashtags = ['#GoPackGo']
	make_request(authorization, hashtags, G)



if  __name__ =='__main__':main()