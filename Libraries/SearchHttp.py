import pandas as pd
from bs4 import BeautifulSoup

import Libraries.ConnectionUrl as connection
import Libraries.ExtractDate as extract
import Libraries.DataframeWork as dfw

# pandas: 
# BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

class SearchHttp:

    connect=""
    extract=""
    dfwork=""

    def ExtractDateBooks(self, arrayBooks):
        
        df = pd.DataFrame(columns = ['Name', 'price', 'rate', 'n_vote', 'link'])
        
        for urlBook in arrayBooks:
            print("Link: ",urlBook)
            
            html = self.connect.returnHtmlUrl(urlBook)
            if (len(html)<1): continue
            soup=BeautifulSoup(html, "html.parser")
            
            # find a list of all span elements
            # create a list of lines corresponding to element texts
            stringTitle = self.extract.titleExtract(soup)
            price       = self.extract.priceExtract(soup)
            rate        = self.extract.rateExtract(soup)
            nvote       = self.extract.voteExtract(soup)
            description = self.extract.descriptionExtract(soup)
            author      = self.extract.authorExtract(soup)
            freqBought  = self.extract.FrequentlyBoughtExtract(soup)

            newline = { 'Name'       : stringTitle,
                        'price'      : price, 
                        'rate'       : rate, 
                        'n_vote'     : nvote,
                        'author'     : author,
                        'description': description,
                        'freqBought' : freqBought,
                        'link'       : urlBook
                        }
            
            # print(pd.Series(newline, index=df.columns))                       
            print("\n")
            df = df.append(newline, ignore_index = True)

        return df

    def fromLink(self, url, writeCsv=False):
        html       = self.connect.returnHtmlUrl(url, timeDelay=5)
        htmlSlpit  = self.extract.splitHtml(html)
        arrayBooks = self.extract.searchHttp(htmlSlpit, nameInLink="amazon")
        df = self.ExtractDateBooks(arrayBooks)

        self.dfwork.showDataFrame(df)
        if(writeCsv): self.dfwork.writeDataFrame(df)

    def fromCsv(self, path, writeCsv=False):
        dfRead     = dfwork.readDataFrame("list_of_trading_books.csv")
        arrayBooks = dfRead["link"]
        df = self.ExtractDateBooks(arrayBooks)

        self.dfwork.showDataFrame(df)
        if(writeCsv): self.dfwork.writeDataFrame(df)

    def __init__(self):
        self.connect = connection.ConnectionUrl()
        self.extract = extract.ExtractDate()
        self.dfwork  = dfw.DataframeWork()
        self.connect.verifyHasConnection()

