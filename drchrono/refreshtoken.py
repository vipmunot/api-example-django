import settings
import time
import requests
import threading

def refreshtoken(isRefresh):
    response = "";
    if(isRefresh):
        response = requests.post('https://drchrono.com/o/token/', data={
            'refresh_token': settings.REFRESH_TOKEN,
            'grant_type': 'refresh_token',
            'client_id': settings.client_id,
            'client_secret': settings.client_secret,
            'redirect_uri' : settings.redirect_uri,
        })
        data = response.json();
        settings.ACCESS_TOKEN = data['access_token'];
        settings.REFRESH_TOKEN = data['refresh_token'];
        settings.ACCESS_TOKEN_EXPIRES_IN = data['expires_in'];
    else:
        response = requests.post('https://drchrono.com/o/revoke_token/', data={
            'client_id': settings.client_id,
            'client_secret': settings.client_secret,
            'token': settings.ACCESS_TOKEN,
        });
        data = response.json()
        print (data)


def countdown_refresh_accesstoken(t):
    t = threading.Timer(t, refreshtoken(True))
    t.daemon = True
    t.start()
