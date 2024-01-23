import requests
from bs4 import BeautifulSoup
import json


def save_json(jfile, data):
    if (data is None) or (len(jfile)==0):
        print("error - no data to save *.json file: jfile={jfile!r};  data == None: {data == None}")
        return
    with open(jfile, 'w', encoding='utf-8') as f:
       f.write(json.dumps(data, indent=2, separators=(",", " : "), ensure_ascii=False))
    print("file: "+ jfile + " saved")


def quotes_to_json(response):
    soup = BeautifulSoup(response.text, 'html.parser') 

    quot_list = []  
    quotes = soup.find_all('span', class_='text')
    authors = soup.find_all('small', class_='author')
    tags = soup.find_all('div', class_='tags')

    for i in range(len(quotes)):
        tags_list = []
        qtags = tags[i].find_all('a', class_='tag')
        for qtag in qtags:
            tags_list.append(qtag.text)

        qd = {"tags": tags_list, "author":  authors[i].text, "quote": quotes[i].text}
        quot_list.append(qd)
    return quot_list


def authors_to_json(response, root):
    soup = BeautifulSoup(response.text, 'html.parser') 

    auth_set = set()
    authors = soup.find_all('small', class_='author')
    for author in authors:
        auth_set.add((author.text, author.parent.find('a')["href"]))

    auth_list = []
    for author in auth_set:
        aurl = root + author[1]
        aresponse = requests.get(aurl)
        asoup = BeautifulSoup(aresponse.text, 'html.parser') 
        adescr = asoup.find('div', class_="author-description").text.strip(' \n')
        aborn = asoup.find('span', class_="author-born-date").text
        aplace = asoup.find('span', class_="author-born-location").text
        
        ad = {"fullname": author[0], "born_date": aborn, "born_location": aplace, "description": adescr}
        auth_list.append(ad)
    return auth_list


def main():
    url = 'https://quotes.toscrape.com/'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"can't get url: {url}")
        exit()

    quotes = quotes_to_json(response)
    save_json("s_qout.json", quotes)
    print("quotes scraped and saved OK")

    authors = authors_to_json(response, url)
    save_json("s_auth.json", authors)
    print("authors scraped and saved OK")
    
    

if __name__ == '__main__':
    main()
