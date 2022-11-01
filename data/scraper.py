from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus
import json
from random import random

from numpy import choose

class Content:
    def __init__(self, title, price, author, description, cover):
        self.title = title
        self.price = price
        self.author = author
        self.description = description
        self.cover = cover
    
    def __str__(self):
        string = "Title: " + self.title + "\n"
        string += "Price: " + self.price + "\n"
        string += "Author: " + self.author + "\n"
        string += "Description: " + self.description + "\n"
        return string
        
    
class Website:
    def __init__(self, name,  url, searchUrl, resultListing, 
              resultUrl, absoluteUrl, titleTag, priceTag, authorTag, descriptionTag, coverTag):
        self.name = name
        self.url = url
        self.searchUrl = searchUrl
        self.resultListing = resultListing
        self.resultUrl = resultUrl
        self.absoluteUrl = absoluteUrl
        self.titleTag = titleTag
        self.priceTag = priceTag
        self.authorTag = authorTag
        self.descriptionTag = descriptionTag
        self.coverTag = coverTag
        
class Crawler:
    def getPage(self, url):
        try:
            html = urlopen(url)
        except HTTPError:
            return None
        except URLError:
            return None
        
        return BeautifulSoup(html, 'html.parser')
    
    def safeGet(self, pageObj, selector):
        childObj = pageObj.select(selector)
        if childObj is not None and len(childObj) > 0:
            return childObj[0].get_text()
        return ""
    
    def search(self, topic, site):
        print(site.searchUrl + topic)
        bs = self.getPage(site.searchUrl + topic)
        result = bs.select(site.resultListing)[0]
        if result is None:
            print("Result not found")
            return
        
        url = result.select(site.resultUrl)[0].attrs['href']
        if (site.absoluteUrl):
            bs = self.getPage(url)
        else:
            bs = self.getPage(site.url + url)
        if bs is None:
            print("Something was wrong with that page or URL. Skipping!")
            return
        
        title = self.safeGet(bs, site.titleTag)
        price = self.safeGet(bs, site.priceTag)
        author = self.safeGet(bs, site.authorTag)
        description = self.safeGet(bs, site.descriptionTag)
        cover = bs.select(site.coverTag)[0].attrs['src']
        
        if title != '' and price != '' and author != '' and description != '' and cover != '':
            content = Content(title, price, author, description, cover)
            return {key: value.strip() for key, value in content.__dict__.items()}
            
                
crawler = Crawler()

info = open('info.json', 'r', encoding='utf-8')
startData = json.load(info)

info.close()

siteData = ['Amazon', 'https://www.amazon.com.br/', 'https://www.amazon.com.br/s?k=', 'div.s-card-container', 'a.a-link-normal', False, '#productTitle', '#price', '.author.notFaded .a-link-normal', '#centerCol .a-expander-content span', '#imgBlkFront']
crawler = Crawler()
site = Website(*siteData)
data = []
categories = ['Melhores Avaliados', 'Mais Vendidos', 'Mais Recentes']
for book in startData:
    print("GETTING DATA ABOUT:", book)
    bookData = crawler.search(quote_plus(book), site)
    choosenCategories = []
    for i in range(3):
        if random() > 0.4:
            choosenCategories.append(categories[i])
    
    print(choosenCategories)
    bookData['categories'] = choosenCategories
    data.append(bookData)

dataFile = open('data.json', 'w')
json.dump(data, dataFile, indent=2)
    