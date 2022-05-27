# author: Bruno Venâncio
# date: 21/01/2022

import Libraries.SearchHttp as sh

link = "http://bettersystemtrader.com/trading-books/"

linkInformation  = sh.SearchHttp()

linkInformation.fromLink(link, writeCsv=True)