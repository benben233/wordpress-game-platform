from wordpress_xmlrpc import Client, WordPressPost, WordPressTerm
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import posts, media, taxonomies
import pandas as pd


client = Client('http://localhost/wordpress/xmlrpc.php', 'user', 'admin')
p = client.call(posts.GetPosts({'number': n}))
for i in [i.id for i in p]:
    client.call(posts.DeletePost(i))

ps = client.call(posts.GetPosts())
client.call(posts.EditPost(p.id, p))

import requests

appid = 1144400
url = "https://steamspy.com/api.php"
parameters = {"request": "appdetails", "appid": appid}
req = requests.get(url, parameters)
{"appid": 1144400, "name": "Senren＊Banka", "developer": "Yuzusoft", "owners": "200000",
 "positive": 7483, "negative": 54}

url = "http://store.steampowered.com/api/appdetails/"
parameters = {"appids": appid}
req = requests.get(url, parameters)
j = req.json()[str(appid)]['data']




