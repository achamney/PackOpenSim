from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from pyquery import PyQuery    
import urllib.request
import requests
import json
from html.parser import HTMLParser
import re


class MyHTMLParser(HTMLParser):
    imgs = []
    foundFigure = False
    inImg = False
    def handle_starttag(self, tag, attrs):
        print(tag)
        if tag == "figure":
            self.foundFigure = True
        if tag == "img" and self.foundFigure:
            self.inImg = True

    def handle_endtag(self, tag):
        if tag == "figure":
            self.foundFigure = False
        if tag == "img":
            self.inImg = False

    def handle_data(self, data):
        if self.inImg:
            print("Encountered some data  :", data)
            self.imgs.append(data)

with sync_playwright() as p:
    imgcounter = 0
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    lastLink = "/wiki/Category:Collectible_cards"
    allLinks = []
    allImgLinks = []
    for i in range(0,50):
        page.goto(f"view-source:https://hearthstone.fandom.com{lastLink}")
        print(f"hi{i}")
        
        parsed_html = PyQuery(page.content())
        thisPageLinks = parsed_html("a")
        for link in thisPageLinks:
            pylink = PyQuery(link)
            if pylink.text()[0:6] == "/wiki/" and pylink.parent().parent().text()[0:3] == "<li":
                lastLink = pylink.text()
                if lastLink[0:len("/wiki/Category:Collectible_cards?pagefrom")] == "/wiki/Category:Collectible_cards?pagefrom":
                    print(lastLink)
                    break
                allLinks.append(lastLink)
        #if lastLink == "/wiki/Category:Collectible_cards?pageuntil=Whack-A-Gnoll+Hammer#mw-pages":
        break
    for link in allLinks:
        print(link)
        thisPage = PyQuery(requests.get(f"https://hearthstone.fandom.com{link}").text)
        thisPageFigure = thisPage("figure")
        #print(len(thisPageFigure))
        try:
            pageImgCount = 0
            #print(thisPage("section h2").outer_html())
            title = PyQuery(thisPage("section h2")[0])
            rarity = thisPage("[data-source='rarity'] div")
            for figure in thisPageFigure:
                pyfigure = PyQuery(figure)
                golden = pyfigure.attr("data-source")
                if golden is None or len(rarity) == 0:
                    continue
                pyimglink = PyQuery(pyfigure.children().children()[0])
                allImgLinks.append({"title": title.text()+str(pageImgCount),
                                    "url":pyimglink.attr("src"), 
                                    "rarity":rarity.text(), 
                                    "golden": "Premium" in golden})
                #print("Premium" in golden)
                pageImgCount += 1
        except Exception as inst:
            print(inst)
            print(f"error getting image {link}")
        
    print(f"writing image links {str(len(allImgLinks))}")
    with open("~/Downloads/temp/imgLinkSet.json", "w") as text_file:
        text_file.write(json.dumps(allImgLinks))
    for imgLink in allImgLinks:
        try:
            urllib.request.urlretrieve(imgLink["url"], f"~/Downloads/temp/{imgLink['title']}.png")
            #print(imgcounter)
            #print(imgLink["title"])
            imgcounter+=1
        except:
            print(imgLink['title'])
            print(imgLink['url'])
            print("error")
