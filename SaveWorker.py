
import os
import threading

from queue import Empty

from sqlalchemy import create_engine
from sqlalchemy.sql import text


class SaveScheduler(threading.Thread):
    def __init__(self, inputQueue, **kwargs):
     
        super(SaveScheduler, self).__init__(**kwargs)
        self._inputQueue = inputQueue
        self.start()

    def run(self):
        while True:
            try:
                val = self._inputQueue.get(timeout=10)
            except Empty:
                print('Timeout, stopping')
                break

            if val == 'DONE':
                break

            companyName, price, extracted_time = val
            saveWorker = SaveWorker(companyName, price, extracted_time)
            saveWorker.AddToDB()


class SaveWorker():
    def __init__(self, companyName, price, extracted_time):
        self._companyName = companyName
        self._price = price
        self._extracted_time = extracted_time

        self._PG_USER = os.environ.get('PG_USER')
        self._PG_PW = os.environ.get('PG_PW')
        self._PG_HOST = os.environ.get('PG_HOST')
        self._PG_DB = os.environ.get('PG_DB')

        self._engine = create_engine(f'postgresql://{self._PG_USER}:{self._PG_PW}@{self._PG_HOST}/{self._PG_DB}')



    def AddToDB(self):
        SQL = """INSERT INTO prices (companyName, price, extracted_time) VALUES 
        (:companyName, :price, :extracted_time)"""
        result={'companyName': self._companyName,
                                              'price': self._price,
                                              'extracted_time': str(self._extracted_time)}
        print(result)
        
        # with self._engine.connect() as conn:
        #     conn.execute(text(SQL), {'companyName': self._companyName,
        #                                       'price': self._price,
        #                                       'extracted_time': str(self._extracted_time)})