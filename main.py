# This is a sample Python script.
import requests
import json
import base64
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

url = "http://localhost/wordpress/index.php/wp-json/wp/v2/posts"

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import posts

client = Client('http://localhost/wordpress/xmlrpc.php', 'user', 'admin')
post = WordPressPost()
post.title = 'My post'
post.content = 'This is a wonderful blog post about XML-RPC.'
post.id = client.call(posts.NewPost(post))

# whoops, I forgot to publish it!
post.post_status = 'publish'
client.call(posts.EditPost(post.id, post))

