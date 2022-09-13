
import threading
from tokenize import Name

import requests
from bs4 import BeautifulSoup


class TableWorker():
    def __init__(self):
       self._url="https://en.wikipedia.org/wiki/List_of_S%26P_500_companies" 
    
    @staticmethod
    def getCompaniesName(pageHtml):
        
        soup = BeautifulSoup(pageHtml)
        table = soup.find(id='constituents')
        table_rows = table.find_all('tr')
        for table_row in table_rows[1:]:
            name = table_row.find('td').text.strip('\n')
            yield name
        

    def requestPage(self):
        res= requests.get(self._url)
        if res.status_code!=200:
           print("something went down!")
           return
        yield from self.getCompaniesName(res.text)