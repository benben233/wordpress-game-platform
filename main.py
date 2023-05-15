import pandas as pd
from wordpress_xmlrpc import Client, WordPressPost, WordPressTerm
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import posts, media, taxonomies
from datetime import datetime

client = Client('http://localhost/wordpress/xmlrpc.php', 'user', 'admin')
games = pd.read_csv('game.csv', index_col='appid')
games = games.fillna('')
games = games.loc[101:]


def post_game(game):
    print(f'Post {game["name"]}')
    post = WordPressPost()
    post.title = game['name']
    post.content = game_content(game)

    post.date = datetime.fromisoformat(game['release_date'])
    post.terms_names = {'post_tag': eval(game['steamspy_tags'])}

    post.custom_fields = [{'key': 'reviews', 'value': float(game['reviews'])},
                          {'key': 'owners', 'value': int(game['owners'])},
                          {'key': 'developer', 'value': game['developer']},
                          {'key': 'appid', 'value': int(game['appid'])}]
    post.excerpt = game['short_description']

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


def get_post(do=None):
    ps = []
    # get pages in batches of 20
    offset = 0
    increment = 20
    while True:
        page = client.call(posts.GetPosts({'number': increment, 'offset': offset}))
        if len(page) == 0:
            break  # no more posts returned
        for p in page:
            do(p)
        ps += page
        offset = offset + increment
    return ps


def edit_game(post):
    print("Edit " + post.title)
    game = games.loc[int(post.custom_fields[0]['value'])]
    post.terms_names = {'category': [game.publisher]}
    post.thumbnail = post.thumbnail['attachment_id']
    client.call(posts.EditPost(post.id, post))


def remove_category(p):
    print("Edit " + p.title)
    t = p.terms
    un = [x for x in t if x.id == '1']
    if len(un) == 0:
        return
    t.remove(un[0])
    p.thumbnail = p.thumbnail['attachment_id']
    client.call(posts.EditPost(p.id, p))


def game_content(game):
    c = f"""<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column -->
<div class="wp-block-column"><!-- wp:button -->
<div class="wp-block-button"><a class="wp-block-button__link" href="{game['website']}">Official Website</a></div>
<!-- /wp:button --></div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column"><!-- wp:paragraph -->
<p>Positive ratings: {game['positive_ratings']}</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Negative ratings: {game['negative_ratings']}</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

"""
    c += game['about_the_game']
    return c

# for n, g in games.iterrows():
#     post_game(g)
get_post()
