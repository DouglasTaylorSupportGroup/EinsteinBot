from bs4 import BeautifulSoup as bs
import re
import json
from core import cookie
from core.scraper import request

with open("config.json", "r") as f:
    config = json.load(f)
cookieStr = cookie.parseCookie("cookie.txt")

def checkLink(link):
    item = re.search('https://www.chegg.com/homework-help/(.*?)/', link)
    if "questions-and-answers" not in item:
        isChapter = True
    else:
        isChapter = False
    return isChapter

def parsePage(html, isChapter):
    soup = bs(html, "html.parser")
    if isChapter:
        token = re.search(r'"token":"(.+?)"', html).group(1)
        chapter_id = str(re.search(r'\?id=(\d+).*?isbn', html).group(1))
        isbn13 = str(re.search(r'"isbn13":"(\d+)"', html).group(1))
        problemId = str(re.search(r'"problemId":"(\d+)"', html).group(1))
        query = {
            "query": {
                "operationName": "getSolutionDetails",
                "variables": {
                    "isbn13": isbn13,
                    "chapterId": chapter_id,
                    "problemId": problemId
                }
            },
            "token": token
        }
        url = 'https://www.chegg.com/study/_ajax/persistquerygraphql'
        answerjson = request.requestChapter(url, cookieStr, config["userAgent"], query, None)
        return answerjson
    else:
        questionhtml = soup.find("div", {"class": "question-body-text"})
        answerhtml = soup.find("div", {"class": "answer-given-body"})
        return questionhtml, answerhtml

def getAnswer(dataRaw, isChapter):
    if isChapter:
        chapter = dataRaw["data"]["textbook_solution"]["chapter"][0]
        question = chapter['problems'][0]
        solution = question['solutionV2'][0]
        return question, solution
    else:
        if 'class="hidden"' in str(dataRaw):
            hidden = dataRaw.find_all("div", {"class": "hidden"})
            for i in hidden:
                i.replace_with("")
        if "<strong>" or "</strong>" in str(dataRaw):
            strong = dataRaw.find_all("strong")
            for i in strong:
                i.replace_with("**" + i.text + "**")
        if "<img>" or "</img>" in str(dataRaw):
            img = dataRaw.find_all("img")
            for i in img:
                url = i["src"]
                i.replace_with(url)
        answerList = []
        for k in dataRaw.contents[1:-1]:
            txt = k.text
            if "\n" in txt and len(txt) > 2:
                newtxt = txt.replace("\n", " ")
                answerList.append(newtxt)
            else:
                answerList.append(txt)
        answerList = [x for x in answerList if x]
        if answerList[0] == "\n":
            answerList = answerList[1:]
        if answerList[-1] == "\n":
            answerList = answerList[:-1]
        return answerList