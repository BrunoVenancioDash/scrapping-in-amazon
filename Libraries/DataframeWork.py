import pandas as pd

class DataframeWork:

    def readDataFrame(self, path):
        return pd.read_csv(path)

    def showBook(self, arrayBooks, show=False):
        if show:
            for book in arrayBooks:
                print(book)
        print("Quantity: ",len(arrayBooks))

    def invalidSizeDataFrame(self, dataFrame):
        if(dataFrame.shape[0]<1):
            print("Error invalid size") 
            return -1
        return 1   

    def showDataFrame(self, dataFrame):
        if(self.invalidSizeDataFrame(dataFrame)<0): return
        print(dataFrame)

    def writeDataFrame(self, dataFrame):
        if(self.invalidSizeDataFrame(dataFrame)<0): return
        dataFrame.to_csv('list_of_trading_books.csv',index=False)