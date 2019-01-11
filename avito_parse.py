import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    r = requests.get(url)
    return r.text
    

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)

def write_csv(data):
    with open('avito.csv', 'a') as f:
        writer= csv.writer(f)
        writer.writerow((data['title'],data['price'],data['metro'],data['url']))

def get_pages_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='catalog-list').find_all('div', class_='item_table')
    for ad in ads:
       	try:
            title = ad.find('div', class_='description').find('h3').text.strip()
        except:
            title = ''
        try:
            url = 'https://avito.ru' + ad.find('div', class_='description').find('h3').find('a').get('href')
        except:
            url = ''
        try:
            price = ad.find('div', class_='about').text.strip()
        except:
            price = ''
        try:
            metro = ad.find('div', class_='data').find_all('p')[-1].text.strip()
        except:
            metro = ''       	
       	try:
       		data = {'title': title,'price': price,'metro': metro,'url': url}
       		write_csv(data)           	
       	except:
       		print('eror')


def main():
    url = 'https://www.avito.ru/moskva/remont_i_stroitelstvo?p=1&q=Ремонт'
    base_url = 'https://www.avito.ru/moskva/remont_i_stroitelstvo?'
    page_part = 'p='
    query_part = '&q=Ремонт'
    total_pages = get_total_pages(get_html(url))
    for i in range(1, total_pages):
            url_gen = base_url + page_part + str(i) + query_part
            print(url_gen)
            html = get_html(url_gen)
            get_pages_data(html) 
if __name__ == '__main__':
    main()
