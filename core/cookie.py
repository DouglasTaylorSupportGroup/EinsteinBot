import requests
from bs4 import BeautifulSoup as bs
import json

# Parses the Cookie for the Chegg Account
def parseCookie(fileName):
    with open(fileName, 'r') as f:
        cookieTxt = f.read()
    cookieRaw = json.loads(cookieTxt)
    cookieString = ""
    z = True
    for cookie in cookieRaw:
        if not z:
            cookieString += "; "
        cookieString += "{name}={value}".format(**cookie)
        z = False
    cookie = cookieString.strip()
    return cookie