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
import requests
from PIL import Image
from io import BytesIO
import os


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
    i=Image.open(f'media/{appid}/header.jpg')
    if i.height == 215 and i.width == 460:
        continue
    else:
        print(f'{appid} Error')
    print('OK')