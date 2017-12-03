import requests
import base64
import json
import networkx as nx
import matplotlib.pyplot as plt



consumer_key = "1ceDRUwTN3nRchujEbjppcukV";
secret_key = "JneAHLQmumCCCMKDocoMCnPDEP88SdmgrjaWZ70Y8FwPbOEBQj";
combined_keys = consumer_key + ":" + secret_key;
encoded_key = "Basic " + base64.b64encode(combined_keys);
#print encoded_key; #MWNlRFJVd1ROM25SY2h1akVianBwY3VrVjpKbmVBSExRbXVtQ0NDTUtEb2NvTUNuUERFUDg4U2RtZ3JqYVdaNzBZOEZ3UGJPRUJRag==

post_headers = {'authorization': encoded_key, 'content-type': 'application/x-www-form-urlencoded;charset=UTF-8'};
post_data = {'grant_type': 'client_credentials'};
pr = requests.post("https://api.twitter.com/oauth2/token", headers=post_headers, data=post_data);
#print (pr.content);
data = json.loads(pr.content)
get_authorization = "Bearer " + data.get("access_token");


payload = {'q': '#GoPackGo', 'result_type': 'popular', 'count': 100}
get_headers = {'authorization': get_authorization}
#r = requests.get('https://api.twitter.com/1.1/search/tweets.json', params=payload)
# ?q=%23freebandnames&since_id=24012619984051000&max_id=250126199840518145&result_type=mixed&count=4')
r = requests.get('https://api.twitter.com/1.1/search/tweets.json?', headers=get_headers, params=payload) #.json?q=%40gudrunvaldis
parsed = json.loads(r.content)
#print(json.dumps(parsed, indent=4))
print(json.dumps(parsed["statuses"], indent=4))
user_tweet = {}
users = []
G = nx.Graph()

for tweet in parsed["statuses"]:
	user_id = tweet["user"]["id"]
	tweet_id = tweet["id_str"]
	user_tweet[user_id] = tweet_id
	users.append(user_id)
	G.add_node(user_id)
	payload1 = {'id': tweet_id}
	headers = {'authorization': get_authorization}
	r = requests.get('https://api.twitter.com/1.1/statuses/retweeters/ids.json', headers=headers, params=payload1)
	retweeters = json.loads(r.content)
	for retweeter in retweeters["ids"]:
		G.add_node(retweeter)
		G.add_edge(user_id, retweeter)

nx.draw(G)
#print(G.edges())
plt.show()
#print (r.url)
#print (r.content)