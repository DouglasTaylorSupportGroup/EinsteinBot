import requests
from bs4 import BeautifulSoup as bs
import json

def parseCookie(fileName):
    with open(fileName, 'r') as f:
        cookie_text = f.read()
    data = json.loads(cookie_text)
    cookie_str = ''
    first_flag = True
    for cookie in data:
        if not first_flag:
            cookie_str += '; '
        cookie_str += '{name}={value}'.format(**cookie)
        first_flag = False
    cookie = cookie_str.strip()
    return cookie

def cookieToDict(cookie: str):
    cookieList = {}
    cookieListRaw = cookie.split(';')
    for cookie in cookieListRaw:
        name, value = cookie.split('=', 1)
        cookieList.update({name.strip(): value.strip()})
    return cookieList