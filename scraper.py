import json
import bs4, requests
import pandas as pd


#Function for later purposes
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

#Read the Url list to be scraped
with open("url_list.txt", "r") as urlFile:
    urlList = [line.strip("\n") for line in urlFile]

#Read selector in input.json
with open("input.json", "r") as f:
    subdict = json.load(f)

#Create Dataframe based on number of selectors, using keys' names specified by user as Headers for the output csv file.
columnList = list(subdict.keys())
columnList.append("url")
df = pd.DataFrame(columns = [columnList])
print(df)

#For loop for every url in url list input -> Generate a response object
index = 0
for url in urlList:
    print("Scraping url: ", url)
    df.loc[index, "url"] = url
    res = requests.get(url)
    scraped_page = bs4.BeautifulSoup(res.text, "html.parser")
    #For Loop: For every response object select html tags according to selectors declared in input.json
    for selector  in subdict:
        if "link" in selector:
            html_box = scraped_page.select(subdict[selector])
            print(f"{selector}: {html_box[0].get("href")}")
            df.loc[index, selector] = html_box[0].get("href")
        elif "text" in selector:
            html_box = scraped_page.select(subdict[selector])
            print(f"{selector}: {html_box[0].getText()}")
            df.loc[index, selector] = html_box[0].getText()
        elif "image" in selector:
            html_box = scraped_page.select(subdict[selector])
            print(f"{selector}: {html_box[0].get("src")}")
            df.loc[index, selector] = html_box[0].get("src")
    index += 1
    print("-----------------------")

#Once all the urls have been scraped, generate a csv file with scraped info
print(df)
df.to_csv("outdf.csv")
