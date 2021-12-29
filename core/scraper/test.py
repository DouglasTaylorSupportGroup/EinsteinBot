import re
import requests
from bs4 import BeautifulSoup as bs
import json

class Scraper:
    
    # Constructor
    def __init__(self, url):
        with open("config.json", "r") as f:
            config = json.load(f)
        self.url = url
        
        # Header used for requests
        self.headers = {
            'authority': 'www.chegg.com',
            "Accept-Encoding": "gzip, deflate, br",
            'accept-language': 'en-US,en;q=0.9',
            'cookie': config["cookie"],
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile': '?0',
            'upgrade-insecure-requests': '1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'user-agent': config["user_agent"],
        }

    # Parses the html with beautiful soup
    def get_soup(html):
        soup = bs(html, "lxml")
        return soup

    # Checks if the url from a chegg site checks if it is a chapter or a question
    def clean_url(url: str):
        is_chapter = False
        match = re.search(r'chegg\.com/homework-help/questions-and-answers/([^?/]+)', url)
        if not match:
            is_chapter = True
            match = re.search(r'chegg\.com/homework-help/[^?/]+', url)
            if not match:
                print('THIS URL NOT SUPPORTED\nurl: {url}')
                return
        return is_chapter, 'https://www.' + match.group(0)

    # Gets the html from the url using requests
    def get_html(self, url):
        return requests.get(url, self.headers).text

    def replace_links(html):
        return re.sub(r'src=\s*?"//(.*)?"', r'src="https://\1"', html)

    # Parses the heading in html on Chegg
    def parse_heading(soup):
        heading = None
        heading_tag = soup.find('span', _class='question-text')
        if heading_tag:
            heading = heading_tag.text
        if not heading:
            meta = soup.find('meta', {'name': 'description'})
            if meta:
                heading = meta.get('content')
        if not heading:
            title = soup.find('title')
            if title:
                heading = title.text
        if not heading:
            print("no heading")
        return str(heading)

    # Finds the Question that was answered in the Chegg Website
    def parse_question(soup, is_chapter):
        if is_chapter:
            question = "<div></div>"
        else:
            question = soup.find('div', {'class': 'question-body-text'})
        return question

    # Parses the answer from the Chegg Website
    def parse_answer(soup, qid, html, url, is_chapter):
        if is_chapter:
            return "fuck"
        token = re.search(r'"token":"(.+?)"', html).group(1)
        return token

    def get_qid(html, is_chapter):
        is_qid = None
        qid = None
        if is_chapter:
            is_qid = True
            data = None
        else:
            try:
                data = json.loads(re.search(r'C\.page\.homeworkhelp_question\((.*)?\);', html).group(1))
                is_qid = True
            except Exception as e:
                print(e)
                is_qid = False

        if is_qid:
            if not is_chapter:
                qid = data['question']['questionUuid']
        else:
            print("no qid")

    #
    def parse(self, html, is_chapter, url):
        html = self.replace_links(html)
        soup = bs(html, 'lxml')
        if soup.find('div', id='px-captcha'):
            print("cap")

        headers = soup.find("head")

        heading = self.parse_heading(soup)

        question = self.parse_question(soup, is_chapter)

        qid = self.get_qid(html, is_chapter)

        answer = self.parse_answer(qid, html, url, is_chapter)

        return headers, heading, question, answer, qid

    def finish(self, url):
        is_chapter, clean_url = self.clean_url(url)
        html = self.get_html(clean_url)
        headers, heading, question, answer, qid = self.parse(html, is_chapter, clean_url)
        return "shit"