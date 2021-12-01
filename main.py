import pandas as pd
from wordpress_xmlrpc import Client, WordPressPost, WordPressTerm
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import posts, media, taxonomies
from datetime import datetime

games = pd.read_csv('game.csv')
games = games.loc[:50]
client = Client('http://localhost/wordpress/xmlrpc.php', 'user', 'admin')


def post_game(game):
    print(f'Post {game["name"]}')
    post = WordPressPost()
    post.title = game['name']
    content = game['about_the_game']
    content = f"Positive ratings: {game['positive_ratings']} Negative_ratings: {game['negative_ratings']}\n" + content
    post.content = content

    post.date = datetime.fromisoformat(game['release_date'])
    post.custom_fields = [{'key': 'reviews', 'value': float(game['reviews'])},
                          {'key': 'owners', 'value': int(game['owners'])},
                          {'key': 'developer', 'value': game['developer']},
                          {'key': 'appid', 'value': int(game['appid'])}]
    post.excerpt = game['short_description']
    # tags = client.call(taxonomies.GetTerms('post_tag'))
    # tag = WordPressTerm()
    # tag.taxonomy = 'post_tag'
    # tag.name = 'My New Tag'
    # tag.id = client.call(taxonomies.NewTerm(tag))
    # prepare metadata

    def post_tag(tags):
        wp_tags = client.call(taxonomies.GetTerms('post_tag'))
        tag = WordPressTerm()
        tag.taxonomy = 'post_tag'
        tag.name = 'My New Tag'
        tag.id = client.call(taxonomies.NewTerm(tag))

    header = {
        'name': f'header-{game["appid"]}.jpg',
        'type': 'image/jpeg',  # mimetype
    }

    # read the binary file and let the XMLRPC library encode it into base64
    with open(f"media/{game['appid']}/header.jpg", 'rb') as img:
        header['bits'] = xmlrpc_client.Binary(img.read())

    response = client.call(media.UploadFile(header))
    post.thumbnail = response['id']

    post.post_status = 'publish'
    post.id = client.call(posts.NewPost(post))
    # client.call(posts.EditPost(p.id,p))


for n, g in games.iterrows():
    post_game(g)
