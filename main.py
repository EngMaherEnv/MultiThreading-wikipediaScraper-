from queue import Queue
import time

from NyseWorker import NysePriceScheduler
from SaveWorker import SaveScheduler

from TableWorker import TableWorker

from multiprocessing import queues

def main():
    startTime=time.time()
    tbWorker=TableWorker()
    namesQueue=Queue()
    SaveQueue=Queue()
    workingNyseThreads=[]
    workingSaveThreads=[]

    numOfNyseThreads=9
    numOfSaveThreads=2

    for name in tbWorker.requestPage():
        namesQueue.put(name)

    #Take the company name and get the price 
    for i in range(numOfNyseThreads):
        nysePriceScheduler=NysePriceScheduler(inputQueue=namesQueue,outputQueue=SaveQueue)
        workingNyseThreads.append(nysePriceScheduler)
    
    # take the final dataRow and save to db 
    for i in range(numOfSaveThreads):
        saveScheduler=SaveScheduler(inputQueue=SaveQueue)
        workingSaveThreads.append(saveScheduler)


    for i in range(len(workingNyseThreads)):
        namesQueue.put("DONE")

    for i in range(len(workingNyseThreads)):
        workingNyseThreads[i].join()
        
    for i in range(len(workingSaveThreads)):
        workingSaveThreads[i].join()

    print(f"Ended in {time.time()- startTime}")





if __name__ == "__main__":
    main()