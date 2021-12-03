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

games = pd.read_csv('game.csv')
g = games.steamspy_tags.apply(eval)
a = []
for x in [x for x in g]:
    a += x
b = set(a)
c = {}
for x in b:
    c[x] = 0
for x in a:
    c[x] += 1
d = sorted(c.items(), key=lambda x: x[1], reverse=True)
print([x[0] for x in d[:20]])
