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

    def ExtractDateBooks(self, arrayBooks):
        
        df = pd.DataFrame(columns = ['Name', 'price', 'rate', 'n_vote', 'link'])

        for urlBook in arrayBooks:
            print("Link: ",urlBook)
            
            html = self.connect.returnHtmlUrl(urlBook)
            if (len(html)<1): continue
            soup=BeautifulSoup(html,"html.parser")
            
            # find a list of all span elements
            # create a list of lines corresponding to element texts
            linesTitle = self.extract.seachSpanFromTag(soup, name='span', class_='class',     tag='a-size-extra-large')
            linesPrice = self.extract.seachSpanFromTag(soup, name='span', class_='class',     tag='a-size-base a-color-price')
            linesRate  = self.extract.seachSpanFromTag(soup, name='span', class_='data-hook', tag='rating-out-of-text')
            linesNvote = self.extract.seachSpanFromTag(soup, name='span', class_='class',     tag='a-size-base a-color-secondary')
            
            stringTitle = linesTitle[0] if (len(linesTitle)>0) else linesTitle

            df = df.append({'Name'  : stringTitle,
                            'price' : linesPrice, 
                            'rate'  : linesRate, 
                            'n_vote': linesNvote,
                            'link'  : urlBook
                        },
                        ignore_index = True)
        print(df)                                    
        return df

    def __init__(self, url):
        self.connect = connection.ConnectionUrl()
        self.connect.verifyHasConnection()
        
        
        html = self.connect.returnHtmlUrl(url, timeDelay=5)
        
        self.extract = extract.ExtractDate()
        htmlSlpit = self.extract.splitHtml(html)

        arrayBooks = self.extract.searchHttp(htmlSlpit, nameInLink="amazon")
        
        df = self.ExtractDateBooks(arrayBooks)
        
        # dfw.DataframeWork().showDataFrame(df)
        dfw.DataframeWork().writeDataFrame(df)
