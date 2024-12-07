BS4 WEB SCRAPER PYTHON SCRIPT  

The script allows to declare the css selectors that point to data that is to be scraped via an input json file.  
  
The URLs that are to be scraped can be declared either as a list of URLs or, if light scraping is to be carried out, as a "Combined Url" like "https://abc.com/page=[1-20]".  
  
In the latter case, the script will parse such "Combined Url" and will proceed to scrape each URL from "https://abc.com/page=1" to "https://abc.com/page=20".  

The user can specify the input url format using a flag upon running the script:  
- "-l": "Combined Url" is provided as input url. (Light scraping).
-  "-p": List of different url is provided as input. (Heavy scraping).
-  In case of no flags provided, user will be prompted with script usage.
  
Once the scraping is carried out, the scraped data will be stored in a output csv file in the script's folder.  
