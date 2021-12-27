import requests
from bs4 import BeautifulSoup as bs
import json

with open("config.json", "r") as f:
    config = json.load(f)

data = json.loads(config["cookie"])
cookie_str = ''
first_flag = True
for cookie in data:
    if not first_flag:
        cookie_str += '; '
    cookie_str += '{name}={value}'.format(**cookie)
    first_flag = False

cookie = cookie_str.strip()
print(cookie)

'''
headers = {
    'authority': 'www.chegg.com',
    # 'cache-control': 'max-age=0',
    "Accept-Encoding": "gzip, deflate, br",
    'accept-language': 'en-US,en;q=0.9',
    'cookie': cookie,
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}
response = requests.get(url="https://www.chegg.com/homework-help/questions-and-answers/4-question-refer-following-declarations-public-class-point-private-double-myx-private-doub-q68966124", headers=headers)
htmlData = response.text
soup = bs(htmlData, "html.parser")
sheesh = soup.find('div', {'class': 'question-body-text'})
print(sheesh)
'''