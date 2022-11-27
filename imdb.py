# https://www.imdb.com/title/tt9114286/
from requests_html import HTMLSession
import time, csv
session = HTMLSession()

def date():
    date = f"[{time.strftime('%d-%m-%y %X')}]"
    return date

def scrape(response):
    try:
        title = response.html.xpath('//h1/text()')[0]
        
        try:
            year = response.html.xpath("(//a[contains(@class,'ipc-link ipc-link--baseAlt')][contains(@href,'tt_ov')])[1]/text()")[0]
        except:
            print(response)
        description = response.html.xpath("//span[@data-testid='plot-l']/text()")[0]
        url_poster = "https://www.imdb.com"+response.html.xpath('(//a[@class="ipc-lockup-overlay ipc-focusable"])[1]')[0].attrs['href']
        response = session.get(url_poster)
        urls = response.html.xpath("(//img[contains(@src,'images')])[1]")
        try:
            url_src = str(urls[0]).split("<Element 'img' src='")[1].split("' srcset='")[0]
        except IndexError:
            url_src = str(urls[0]).split("<Element 'img' class=('sc-7c0a9e7c-0', 'hXPlvk', 'peek') src='")[1].split("' srcset='")[0]
        except Exception as e:
            print(f'{date()} Something Err: {e}')
            
        id = url_poster.split("/title/")[1].split('/mediaviewer/')[0]
        return ([f"{title} ({year})",year,description,url_src,id])
    except IndexError:
        pass

def main(i):
    try:
        response = session.get(i)
        dict_data = scrape(response)
        print(f'{date()} [ID: {dict_data[4]} ] Successfully scrapped ')
        return dict_data
    except IndexError:
        pass

if __name__ == '__main__': 
    global save_file
    print(f'{date()} ImDB Scrapper')
    datas = input(f'{date()} Folder ID/URL: ')
    save_file = input(f'{date()} File to save (csv): ')
    data = f"{datas}"
    file = open(f"./{data}","r")
    list_ids = file.read()
    list_id = list_ids.split("\n")
    with open(save_file, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        for i in list_id:
            try:
                if "https://www.imdb.com" not in i:
                    i = "https://www.imdb.com/title/"+i
                writer.writerow(main(i))
            except ConnectionAbortedError or ConnectionError or ConnectionRefusedError or ConnectionResetError:
                print(f'{date()} Connection Error')
                input(f'{date()} Enter to Continue or CTRL + C to Exit')
            except IndexError:
                pass
