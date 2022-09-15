The project works as follows: 
- main() will run the TabelWorker to scrap  a table on the Wikipedia page: https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
- The TablWorker will put the company name scraped into the namesQueue
- Then many threads will start consuming from the namesQueue (it will get the name and add it to the end of this URL: "https://www.nyse.com/quote/XNYS:" and scrap the price
 )  
- NysePriceScheduler threads will put DataRow(name, price, scrap time) to the output queue called SaveQueue.
- Finally, the saveWorker will create many Threads to save the DataRow consumed from the SaveQueue into DB 
This is a brief summary only. Details of how the threads Scheduler operate and start the threads, when they stop, join together, and how thread's data are passed down to other classes can only be seen in the implementation and code comments.
