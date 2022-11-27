from requests_html import HTMLSession
session = HTMLSession()
import time, csv
from time import sleep
headers = {
    'authority': 'www.themoviedb.org',
    'accept': 'text/html, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8,id;q=0.7',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'tmdb.prefs=%7B%22adult%22%3Afalse%2C%22i18n_fallback_language%22%3A%22en-US%22%2C%22locale%22%3A%22en-US%22%2C%22country_code%22%3A%22ID%22%2C%22timezone%22%3A%22Asia%2FJakarta%22%7D; tmdb.session=AVMXGOSaGogfJzIxPzBUFAcm6byPUXk3hXhWlCiEJKepOGUmm5TPFKmYRdLambDWiQkf3_PjrJR-sBqM3ALdURMXzRxU41tPZnFsLuu7IzNgvUP8kNlDG_Xj4hZvWGJ9chcjdrsK0_i7tsBulQvIRkfQNY_1wjO6lZiwwOsj18zgpiBU_WSJPfYAcsM0OFn9ejT3jZ2A8rb3ttlzia2yjJBxrWqt7n_G4Zm6Ls_WZrMH',
    'dnt': '1',
    'origin': 'https://www.themoviedb.org',
    'referer': 'https://www.themoviedb.org/movie/?fbclid=IwAR04lWCuwrl9f7CH0RWpoeRC8Slzte4EWWoQPORr_b4RCbSAOozPWJ9nR48',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

def date():
    date = f"[{time.strftime('%d-%m-%y %X')}]"
    return date

def scrapper(page):
    data = {
        'air_date.gte': '',
        'air_date.lte': '',
        'certification': '',
        'certification_country': 'ID',
        'debug': '',
        'first_air_date.gte': '',
        'first_air_date.lte': '',
        'ott_region': 'ID',
        'page': page,
        'primary_release_date.gte': '',
        'primary_release_date.lte': '',
        'region': '',
        'release_date.gte': '',
        'release_date.lte': '',
        'show_me': '0',
        'sort_by': 'popularity.desc',
        'vote_average.gte': '0',
        'vote_average.lte': '10',
        'vote_count.gte': '',
        'with_genres': '',
        'with_keywords': '',
        'with_networks': '',
        'with_origin_country': '',
        'with_original_language': '',
        'with_ott_monetization_types': '',
        'with_ott_providers': '',
        'with_release_type': '',
        'with_runtime.gte': '0',
        'with_runtime.lte': '400',
    }

    response = session.post('https://www.themoviedb.org/discover/movie/items', headers=headers, data=data)
    url_movie = response.html.xpath("//a[contains(@href,'/movie')]")
    
    for e,i in enumerate(url_movie):
        try:
            url = i.attrs['href']
            response = session.get(f'https://www.themoviedb.org{url}')
            get_title = response.html.xpath('//span[@class="tag release_date"]/preceding-sibling::a/text()')[0]
            year = response.html.xpath('//span[@class="tag release_date"]/text()')[0].replace("(","").replace(")","")
            title = f"{get_title} ({year})"
            # rating = response.html.xpath('//span[contains(@class,"icon icon-r")]')[0].attrs['class']
            url_src = "https://www.themoviedb.org"+response.html.xpath('(//img[contains(@class,"poster")])[1]')[0].attrs['data-src']
            id_movie = url.split('/movie/')[1]
            description = response.html.xpath('//div[@class="overview"]/p/text()')[0]
            get_genre = response.html.xpath('//span[@class="genres"]/a/text()')
            genre = ""
            for gen in get_genre:
                genre = gen + ", " + genre
            if e % 2 == 0:
                print(f'{date()} [ID: {id_movie} ] Successfully scrapped ')
                with open('result.txt','a',encoding='utf-8') as f:
                    f.write(f'{title}|{year}|{description}|{id_movie}|{genre}|{url_src}\n')
        except IndexError:
            pass
        except ConnectionAbortedError or ConnectionError or ConnectionRefusedError or ConnectionResetError:
            print(f'{date()} Connection Error')
            input(f'{date()} Enter to Continue or CTRL + C to Exit')
if __name__ == '__main__': 
    print(f'{date()} TmDB Scrapper')
    start_at = int(input(f'{date()} Start Page: '))
    end_at = int(input(f'{date()} End Page: '))
    for i in range(start_at,end_at+1):
        try:
            scrapper(i)
        except ConnectionAbortedError or ConnectionError or ConnectionRefusedError or ConnectionResetError:
            print(f'{date()} Connection Error')
            input(f'{date()} Enter to Continue or CTRL + C to Exit')
