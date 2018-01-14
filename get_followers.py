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


def make_request(auth, user, graph):
	payload = {'user_id': user, 'count': 500}
	get_headers = {'authorization': auth}
	r = requests.get('https://api.twitter.com/1.1/followers/ids.json?', headers=get_headers, params=payload)
	parsed = json.loads(r.content).get('ids')
	weights_dict = get_weights(auth, parsed, graph)
	#showGraph(graph)
	#return graph
	for key, value in sorted(weights_dict.iteritems(), key=lambda (k,v): (v,k)):
   		print "%s: %s" % (key, value)


def get_weights(auth, followers, G):
	user_tweet = {}
	users = []
	user_weights = {}

	for follower in followers:
		#users.append(user_id)
		weight = model1.userScore(follower)
		user_weights[follower] = weight

	return user_weights
		#G.add_node(follower, node_size=weight_user)
		#return G

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
	user_id = ['25073877']
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


	gr = make_request(authorization, user_id, G)




	#print hashtags




if  __name__ =='__main__':main()