import pandas as pd

class ExtractDate(object):

    def splitHtml(self, data):
        data = data.replace('"',"'") # " => '
        data = data.replace(" ","'") # space => '
        data = data.split("'")
        
        return [data]

    def searchHttp(self, data, nameInLink=""):
        arrayBooks = self.for2Condition(data, nameInLink) if (len(nameInLink)>0) else self.for1Condition(data) 
        return arrayBooks

    def for1Condition(self, data):
        f = lambda  x, cond : 'http' in x
        array = filter(f, data[0])
        return array
    
    def for2Condition(self, data, nameInLink):
        array = []
        for line in data[0]:
            if 'http' in line and nameInLink in line:
                array.append(line)
        return array

    def is_float(self, element):
        try:
            float(element)
            return True
        except ValueError:
            return False

    def priceTransformation(self, price):
        if(len(price)<1): return price
        priceArray = [ x.replace("$","") for x in price]
        priceArray = [ float(x) for x in priceArray if self.is_float(x)]
        return priceArray

    def rateTransformation(self, rate, percent=False):
        if (len(rate)<1): return rate
        transf1 = rate[0].replace("[","")
        transf1 = transf1.split(" ")
        rateNew = float(transf1[0]) if self.is_float(transf1[0]) else 0
        rateNew = rateNew/5.0 if(percent) else rateNew
        return rateNew

    def voteTransformation(self, nvote):
        if(len(nvote)<1): return nvote
        nvoteSplit = nvote[-1].split(" ")
        nvoteString = nvoteSplit[-3].replace(",","")
        nvote = int(nvoteString)
        return nvote

    def descriptionTransformation(self, line):
        description = line 
        return description 

    def authorTransformation(self, line):
        auhtors = line
        return auhtors

    def FrequentlyBoughtTransformation(self, line):
        frequentlyBought = line
        return frequentlyBought

    def seachSpanFromTag(self, 
                        soupHtml, 
                        name, 
                        class_,
                        tag
                        ):
        spans = soupHtml.find_all(name, {class_ : tag})
        lines = [span.get_text() for span in spans]
        
        return lines

    def titleExtract(self, soup):
        lines = self.seachSpanFromTag(soup, name='span', class_='class',     tag='a-size-extra-large')
        line  = lines[0] if (len(lines)>0) else lines
        return line

    def priceExtract(self, soup):
        lines = self.seachSpanFromTag(soup, name='span', class_='class',     tag='a-size-base a-color-price')
        line  = self.priceTransformation(lines)
        return line

    def rateExtract(self, soup):        
        lines = self.seachSpanFromTag(soup, name='span', class_='data-hook', tag='rating-out-of-text')
        line  = self.rateTransformation(lines, percent=True)
        return line

    def voteExtract(self, soup):        
        lines = self.seachSpanFromTag(soup, name='span', class_='class',     tag='a-size-base a-color-secondary')
        line  = self.voteTransformation(lines)
        return line

    def descriptionExtract(self, soup):        
        lines = self.seachSpanFromTag(soup, name='div', class_='class',     tag='a-section a-spacing-none a-text-center rpi-attribute-value')
        line  = self.descriptionTransformation(lines)
        return line

    def authorExtract(self, soup):
        lines = self.seachSpanFromTag(soup, name='a', class_='class',     tag='a-size-large a-link-normal')
        line  = self.authorTransformation(lines)
        return line

    def FrequentlyBoughtExtract(self, soup):
        lines = self.seachSpanFromTag(soup, name='span', class_='class',     tag='_p13n-desktop-sims-fbt_fbt-desktop_title-truncate__1pPAM')
        line  = self.FrequentlyBoughtTransformation(lines)
        return line