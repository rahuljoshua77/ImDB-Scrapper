# https://www.imdb.com/title/tt9114286/
from requests_html import HTMLSession
import time, csv
session = HTMLSession()

def date():
    date = f"[{time.strftime('%d-%m-%y %X')}]"
    return date

def scrape(response):
    title = response.html.xpath('//h1/text()')[0]
    year = response.html.xpath('(//h1/following-sibling::div/ul/li/a)[1]/text()')[0]
    description = response.html.xpath("//span[@data-testid='plot-l']/text()")[0]
    url_poster = "https://www.imdb.com"+response.html.xpath('(//a[@class="ipc-lockup-overlay ipc-focusable"])[1]')[0].attrs['href']
    response = session.get(url_poster)
    urls = response.html.xpath("(//img[contains(@src,'images')])[1]")
    url_src = str(urls[0]).split("<Element 'img' src='")[1].split("' srcset='")[0]
    id = url_poster.split("/title/")[1].split('/mediaviewer/')[0]
    return dict({'title':f"{title} ({year})",
                 'year':year,
                 'description':description,
                 'url_poster':url_src,
                 'id':id
                })

def main(i):
    response = session.get(i)
    dict_data = scrape(response)
    print(f'{date()} [ID: {dict_data["id"]} ] Successfully scrapped ')
    with open(save_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['title','year','description','url_poster','id'])
        writer.writeheader()
        for data in [dict_data]:
            writer.writerow(data)


if __name__ == '__main__': 
    global save_file
    print(f'{date()} ImDB Scrapper')
    datas = input(f'{date()} Folder ID/URL: ')
    save_file = input(f'{date()} File to save (csv): ')
    data = f"{datas}"
    file = open(f"./{data}","r")
    list_ids = file.read()
    list_id = list_ids.split("\n")
    for i in list_id:
        if "https://www.imdb.com" not in i:
            i = "https://www.imdb.com/title/"+i
        main(i)
