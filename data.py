# import requests
#
# appid = 1144400
# url = "https://steamspy.com/api.php"
# parameters = {"request": "appdetails", "appid": appid}
# req = requests.get(url, parameters)
# {"appid":1144400,"name": "Senren＊Banka" ,"developer":"Yuzusoft","owners":"200000",
#  "positive":7483,"negative":54 }
#
# url = "http://store.steampowered.com/api/appdetails/"
# parameters = {"appids": appid}
# req = requests.get(url, parameters)
# j = req.json()[str(appid)]['data']

import requests
from PIL import Image
from io import BytesIO
import os
from collections import Counter
import pandas as pd

df = pd.read_csv('steam/steam.csv', index_col='appid')
rate = df[['name', 'positive_ratings', 'negative_ratings', 'owners']].copy()
rate = rate[rate['positive_ratings'] > 500]

rate['reviews'] = rate['positive_ratings'] / (rate['positive_ratings'] + rate['negative_ratings'])
rate['owners'] = rate['owners'].apply(lambda x: x.split('-')[1])
rate = rate[(rate.reviews > 0.9) | (rate.owners.astype(int) > 1000000)]
rate.to_csv('rate.csv')
# rate = pd.read_csv('rate.csv', index_col='appid')
game = rate.join(df[['release_date', 'developer', 'steamspy_tags']])
description = pd.read_csv('steam/steam_description_data.csv', index_col='steam_appid',
                          usecols=['steam_appid', 'about_the_game', 'short_description'])
game = game.join(description.rename_axis('appid'))

media = pd.read_csv('steam/steam_media_data.csv', index_col='steam_appid',
                    usecols=['steam_appid', 'header_image', 'background'])
game = game.join(media.rename_axis('appid'))
support = pd.read_csv('steam/steam_support_info.csv', index_col='steam_appid',
                      usecols=['steam_appid', 'website'])
game = game.join(support.rename_axis('appid'))
game['steamspy_tags'] = game['steamspy_tags'].apply(lambda x: x.split(';'))
game.to_csv('game.csv')

media = pd.read_csv('game.csv', index_col='appid', usecols=['appid', 'header_image', 'background'])
for appid, img in media.iterrows():
    path = f'media/{appid}'
    if not os.path.isdir(path):
        os.mkdir(path)
        print(f'download image of {appid}')
        req = requests.get(img[0])
        if req.ok:
            header = Image.open(BytesIO(req.content))
            header.save(path + '/header.jpg')
        else:
            print(f'Error: {req.status_code}')
        req = requests.get(img[1])
        if req.ok:
            background = Image.open(BytesIO(req.content))
            background.save(path + '/background.jpg')
        else:
            print(f'Error: {req.status_code}')

for appid in game.appid:
    i = Image.open(f'media/{appid}/header.jpg')
    if i.height == 215 and i.width == 460:
        continue
    else:
        print(f'{appid} Error')
    print('OK')


def count_element(data: pd.Series):
    li = []
    if type(data.iloc[0]) == str:
        for row in data:
            li += [row]
    else:
        for row in data:
            li += row
    c = Counter(li)
    return pd.DataFrame.from_dict(dict(c), 'index')[0]


tags = count_element(game['steamspy_tags'].apply(eval))
tags = tags[tags > 2].sort_values(ascending=False)
publishers = count_element(game['publisher'])
publishers = publishers[publishers > 2].sort_values(ascending=False)

with open('html/publishers_tags.json','w') as f:
    f.write(f"[{publishers.to_json()},{tags.to_json()}]")

# games = pd.read_csv('game.csv')
# g = games.steamspy_tags.apply(eval)
# a = []
# for x in [x for x in g]:
#     a += x
# b = set(a)
# c = {}
# for x in b:
#     c[x] = 0
# for x in a:
#     c[x] += 1
# d = sorted(c.items(), key=lambda x: x[1], reverse=True)
# print([x[0] for x in d[:20]])
