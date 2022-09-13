import datetime
from re import L
import threading
from time import sleep

from lxml import html
import requests
import random


class NysePriceScheduler(threading.Thread):
    def __init__(self, inputQueue,outputQueue, **kwargs):
        super(NysePriceScheduler, self).__init__(**kwargs)
        self._inputQueue = inputQueue
    
        self._outputQueues = outputQueue
        self.start()
    
    def run(self):
        while True:
            name=self._inputQueue.get()
            if name =="DONE":
                if self._outputQueues is not None:
                    self._outputQueues.put("DONE")
                break
            nyseWorker=NyseWorker(companyName=name)
            price=nyseWorker.getPrice()
            
            dataRow = (name, price, datetime.datetime.utcnow())
            self._outputQueues.put(dataRow)

class NyseWorker():
    def __init__(self,companyName,**kwargs):
        self._companyName=companyName
        baseUrl="https://www.nyse.com/quote/XNYS:"
        self._url=f"{baseUrl}{self._companyName}"
    
    def getPrice(self):
        r=requests.get(self._url)
        page=html.fromstring(r.text)
        #here we scrap the page but some times the Html changes so to make sure we will get a randowm float for now 
        # price=float(page.xpath("/html/body/div[1]/div[3]/div[3]/div/div/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[2]/span[1]")[0].text)
        price=random.random()
        return price

