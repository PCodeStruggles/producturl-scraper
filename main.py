import json
import requests
import bs4
import sys
import pandas as pd

def usage():
    print("--------USAGE--------")
    print("Please provide one of the following flag upon running the script:")
    print("'-p' -> heavy scraping")
    print("'-l' -> light scraping")
    print("Ex. 'python3 [python_script].py -p|-l'")


#Extract url from regex ["first_page"-"last_page"]
def extract_url(url):
    out = []
    result = []
    url = list(url)
    first_page = int(url[(url.index("[")) + 1])
    last_page_list = url[(url.index("[") +3): url.index("]")]
    last_page_raw = map(str, last_page_list)
    last_page = "".join(last_page_raw)
    last_page = int(last_page)
    for i in range(first_page, last_page + 1):
        del url[(url.index("[") +1) : url.index("]")]
        url.insert(url.index("[") + 1, i)
        url_string = map(str, url)
        out.append("".join(url_string))
    for item in out:
        x = item.replace("[", "")
        y = x.replace("]", "")
        result.append(y)
    return result

#Initialize Dataframe to collect scraped data
df = pd.DataFrame()
i = int(0)

#Importing json file where selectors are declared
with open("input.json", "r") as selectors_file:
    scrape_env = json.load(selectors_file)

#Inner useful variables
keys = list(scrape_env.keys())
excl_keys = ["url", "box"]

#Creating a dict with selectors only (therefore excluding "url" and "box")
selectors_dict = {key: scrape_env[key] for key in scrape_env if key not in excl_keys}

#Checking scraping type through flags ('-l' -> light scraping | '-p' -> heavy scraping)
try:
    #Light scraping
    if sys.argv[1] == "-l":
        urls_list = extract_url(scrape_env["url"])
        for url in urls_list:
            print("Scraping url: ", url)
            scraped_page = requests.get(url)
            scraped_page_soup  = bs4.BeautifulSoup(scraped_page.text, "html.parser")
            print("--------------------")
            for box in scraped_page_soup.select(scrape_env["box"]):
                for selector in selectors_dict:
                    if selectors_dict[selector][1] == "getText":
                        print(selector, box.select_one(selectors_dict[selector][0]).getText())
                        df.loc[i, keys[0]] = url
                        df.loc[i, selector] = box.select_one(selectors_dict[selector][0]).getText()
                    else:
                        print(selector, box.select_one(selectors_dict[selector][0]).get(selectors_dict[selector][1]))
                        df.loc[i, keys[0]] = url
                        df.loc[i, selector] = box.select_one(selectors_dict[selector][0]).get(selectors_dict[selector][1])
                print("--------------------")
                i += 1

    #Heavy scraping
    elif sys.argv[1] == "-p":
        urls_list = scrape_env["url"]
        for url in urls_list:
            print("Scraping url: ", url)
            scraped_page = requests.get(url)
            scraped_page_soup  = bs4.BeautifulSoup(scraped_page.text, "html.parser")
            print("--------------------")
            for selector in selectors_dict:
                if selectors_dict[selector][1] == "getText":
                    print(selector, scraped_page_soup.select_one(selectors_dict[selector][0]).getText())
                    df.loc[i, keys[0]] = url
                    df.loc[i, selector] = scraped_page_soup.select_one(selectors_dict[selector][0]).getText()
                else:
                    print(selector, scraped_page_soup.select_one(selectors_dict[selector][0]).get(selectors_dict[selector][1]))
                    df.loc[i, keys[0]] = url
                    df.loc[i, selector] = scraped_page_soup.select_one(selectors_dict[selector][0]).get(selectors_dict[selector][1])
            print("--------------------")
            i += 1

except:
    print("!! NO FLAG PROVIDED !!")
    usage()


df.to_csv("scraped_data.csv")
