import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
import re
import time


class SearchHttp:
    
    def verifyHasConnection(self, timeout=5):
        try:
            request = requests.get("http://www.google.com", timeout=timeout)
            print("Connected to the Internet ...")
        except (requests.ConnectionError, requests.Timeout) as exception:
            print( "No internet connection ...")


    def returnHtmlUrl(self, url, timeDelay=1):
        time.sleep(timeDelay)
        try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req,timeout=10).read()
        except:
            print("Error to download html form site")
            return ""
        
        return webpage.decode("utf-8")
        
    def slpitHtml(self, data):
        print(type(data))
        data = data.replace('"',"'") # " => '
        data = data.replace(" ","'") # space => '
        data = data.split("'")
        
        return [data]

    def for1Condition(self, data):
        array = []
        for line in data[0]:
            if 'http' in line:
                array.append(line)
        return array

    def for2Condition(self, data, nameInLink):
        array = []
        for line in data[0]:
            if 'http' in line and nameInLink in line:
                array.append(line)
        return array

    def searchHttp(self, data, nameInLink=""):
        self.arrayBooks = self.for2Condition(data, nameInLink) if (len(nameInLink)>0) else self.for1Condition(data) 
        
    def showBook(self, show=False):
        if show:
            for book in self.arrayBooks:
                print(book)
        print("Quantity: ",len(self.arrayBooks))

    def seachSpanFromTag(self, 
                        soupHtml, 
                        name ='span', 
                        class_ ='class',
                        tag = ''
                        ):
        spans = soupHtml.find_all(name, {class_ : tag})
        lines = [span.get_text() for span in spans]
        
        return lines

    def ExtractDate(self):
        for urlBook in self.arrayBooks[:5]:
            print("Link",urlBook)
            
            html = self.returnHtmlUrl(urlBook)

            if (len(html)==0): continue
            soup=BeautifulSoup(html,"html.parser")
            
            # find a list of all span elements
            # create a list of lines corresponding to element texts
            linesTitle = self.seachSpanFromTag(soup, name='span', class_='class', tag='a-size-extra-large')
            linesPrice = self.seachSpanFromTag(soup, name='span', class_='class', tag='a-size-base a-color-price')
            linesRate  = self.seachSpanFromTag(soup, name='span', class_='data-hook', tag='rating-out-of-text')
            linesNvote = self.seachSpanFromTag(soup, name='span', class_='class', tag='a-size-base a-color-secondary')

            self.df = self.df.append({  'Name'  : linesTitle[0],
                                        'price' : linesPrice, 
                                        'rate'  : linesRate, 
                                        'n_vote': linesNvote,
                                        'link'  : urlBook
                                    },
                                    ignore_index = True)

    def showDataFrame(self):
        print(self.df)

    def writeDataFrame(self):
        self.df.to_csv('list_of_trading_books.csv',index=False)

    def __init__(self, url):
        
        self.verifyHasConnection(5)

        self.arrayBooks = []
        self.df = pd.DataFrame(columns = ['Name', 'price', 'rate', 'n_vote', 'link'])

        html      = self.returnHtmlUrl(url, timeDelay=5)
        htmlSlpit = self.slpitHtml(html)
        self.searchHttp(htmlSlpit, nameInLink="amazon")
        self.showBook()
        self.ExtractDate()
        self.showDataFrame()
        self.writeDataFrame()
