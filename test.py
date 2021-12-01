from wordpress_xmlrpc import Client, WordPressPost, WordPressTerm
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import posts, media, taxonomies
client = Client('http://localhost/wordpress/xmlrpc.php', 'user', 'admin')
p=client.call(posts.GetPosts({'number': n}))
for i in [i.id for i in p ]:
    client.call(posts.DeletePost(i))