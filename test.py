import requests

appid = 1144400
url = "https://steamspy.com/api.php"
parameters = {"request": "appdetails", "appid": appid}
req = requests.get(url, parameters)
# {"appid":1144400,"name": "Senren＊Banka" ,"developer":"Yuzusoft","owners":"200000",
#  "positive":7483,"negative":54 }

url = "http://store.steampowered.com/api/appdetails/"
parameters = {"appids": appid}
req = requests.get(url, parameters)
j = req.json()[str(appid)]['data']

