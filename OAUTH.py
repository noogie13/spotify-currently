import time
import credentials
import os
from os import path
import webbrowser
import base64
import requests
from json import dump, load
from urllib.parse import urlencode, urlparse

class OAUTH:
    def __init__(self):
        self.client_id = credentials.id
        self.client_secret = credentials.secret
        self.redirect_uri = credentials.redirect
        self.base64_encoded = base64.b64encode((self.client_id + ':' + self.client_secret).encode('ascii'))
        self.scope = 'user-read-currently-playing'

        if path.exists('token.json'):
            with open('token.json') as jsonfile:
                self.token = load(jsonfile)
                if self.token_age() > 3600:
                    self.refresh_token()
        else:
            self.code = self.get_code_web()
            self.token = self.get_token()

    def token_age(self):
        return time.time() - path.getmtime('token.json')

    def get_token(self):
        if self.code == False:
            get_code_web()
        url = 'https://accounts.spotify.com/api/token'
        headers = {'Authorization':'Basic '+self.base64_encoded.decode('ascii')}
        data = {
            'grant_type':'authorization_code',
            'code':self.code,
            'redirect_uri':self.redirect_uri
        }
        token_request = requests.post(url, headers=headers, data=data)
        with open('token.json','w') as jsonfile:
            dump(token_request.json(), jsonfile)
        return token_request.json()

    def refresh_token(self):
        url = 'https://accounts.spotify.com/api/token'
        refresh_token = self.token['refresh_token']
        headers = {'Authorization':'Basic '+self.base64_encoded.decode('ascii')}
        data = {
            'grant_type':'refresh_token',
            'refresh_token':refresh_token
        }
        token_request = requests.post(url, headers=headers, data=data)
        token_json = token_request.json()
        token_json['refresh_token'] = refresh_token
        with open('token.json','w') as jsonfile:
            dump(token_json, jsonfile)
        self.token = token_json

    def get_code_web(self):
        webbrowser.open('https://accounts.spotify.com/authorize?'
                        + urlencode({
                        'response_type' : 'code',
                        'client_id' : self.client_id,
                        'scope' : self.scope,
                        'redirect_uri' : self.redirect_uri
                        }))
        redirected_link = input("Enter the link that you were redirected to: ")
        return urlparse(redirected_link).query[5:]
