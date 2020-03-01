#!/usr/bin/python3
import OAUTH
import requests

id = 'ENTER ID'

secret = 'ENTER SECRET'

redirect = 'ENTER REDIRECT'

scopes = 'user-read-playback-state user-read-currently-playing user-modify-playback-state'


user = OAUTH.OAUTH(id, secret, redirect, scopes)

isplaying = requests.get('https://api.spotify.com/v1/me/player',
                         headers={'Authorization':'Bearer '
                                  + user.token['access_token']}).text

currently = requests.get('https://api.spotify.com/v1/me/player/currently-playing',
                         headers={'Authorization':'Bearer '
                                  + user.token['access_token']}).json()

print(currently['item']['artists'][0]['name'] + ' - ' + currently['item']['album']['name'])

# ['item']['album']['images'][0]['url']
