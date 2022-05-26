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

    def seachSpanFromTag(self, 
                        soupHtml, 
                        name, 
                        class_,
                        tag
                        ):
        spans = soupHtml.find_all(name, {class_ : tag})
        lines = [span.get_text() for span in spans]
        
        return lines
