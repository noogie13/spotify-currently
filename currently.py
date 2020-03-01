#!/usr/bin/python3
import OAUTH
import requests

user = OAUTH.OAUTH()

currently = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers={'Authorization':'Bearer ' + user.token['access_token']}).json()

print(currently['item']['artists'][0]['name'] + ' - ' + currently['item']['album']['name'])

# ['item']['album']['images'][0]['url']

