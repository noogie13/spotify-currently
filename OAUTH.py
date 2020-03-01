import time
from os import path
import webbrowser
import base64
import requests
from json import dump, load
from urllib.parse import urlencode, urlparse

class OAUTH:
    def __init__(self,id, secret, redirect, scope):
        self.client_id = id
        self.client_secret = secret
        self.redirect_uri = redirect
        self.base64_encoded = base64.b64encode((self.client_id + ':' + self.client_secret).encode('ascii'))
        self.scope = scope
        if path.exists('token.json'):
            with open('token.json') as jsonfile:
                self.token = load(jsonfile)
            if self.token_age() > 3600:
                self.token = self.refresh_token()
        else:
            self.code = self.get_code_web()
            self.token = self.get_token()
        self.write_token()

    def token_age(self):
        return abs(time.time() - self.token['time'])

    def write_token(self):
        self.token['time'] = time.time()
        with open('token.json','w') as jsonfile:
            dump(self.token, jsonfile)

    def get_token(self):
        url = 'https://accounts.spotify.com/api/token'
        headers = {'Authorization':'Basic '+self.base64_encoded.decode('ascii')}
        data = {'grant_type':'authorization_code',
                'code':self.code,
                'redirect_uri':self.redirect_uri}
        token_request = requests.post(url, headers=headers, data=data)
        return token_request.json()

    def refresh_token(self):
        url = 'https://accounts.spotify.com/api/token'
        refresh_token = self.token['refresh_token']
        headers = {'Authorization':'Basic '+self.base64_encoded.decode('ascii')}
        data = {'grant_type':'refresh_token',
                'refresh_token':refresh_token}
        token_request = requests.post(url, headers=headers, data=data)
        token_json = token_request.json()
        if 'refresh_token' not in token_json:
            token_json['refresh_token'] = refresh_token
        return token_json

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
