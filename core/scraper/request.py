import requests
from requests_html import HTMLSession
    
def requestWebsite(url, cookie, userAgent):
    headers = {
        'Host': 'www.chegg.com',
        'authority': 'www.chegg.com',
        "Accept-Encoding": "gzip, deflate, br",
        'accept-language': 'en-US,en;q=0.5',
        'cookie': cookie,
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'user-agent': userAgent,
        'referer': 'https://www.google.com/'
    }
    response = requests.get(url=url, headers=headers)
    return response.text
    
def requestChapter(url, cookie, userAgent, json, data):
    headers = {
        'Host': 'www.chegg.com',
        'authority': 'www.chegg.com',
        "Accept-Encoding": "gzip, deflate, br",
        'accept-language': 'en-US,en;q=0.5',
        'cookie': cookie,
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'user-agent': userAgent,
        'referer': 'https://www.google.com/'
    }
    response = requests.post(url=url, headers=headers, json=json, data=data)
    return response.json()