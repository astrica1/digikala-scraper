from bs4 import BeautifulSoup
import requests
import urllib.request, urllib.parse
from os.path import basename
import time
from joblib import Parallel, delayed
import asyncio

def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)
    return wrapped


#region Background Downloader
def SaveImage(url):
    try:
        url = urllib.parse.urljoin(url, urllib.parse.urlparse(url).path)
        name = 'images/' + basename(urllib.parse.urlparse(url).path)
        urllib.request.urlretrieve(url, name)
    except:
        print('exception in save')
        time.sleep(1)
        SaveImage(url)

@background     
def BackgroundImageExtractor(url):
    try:
        HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})
        webpage = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, 'lxml')
        images = soup.find_all('div', class_=['c-remodal-gallery__main-img', 'js-gallery-main-img'])
        attrs = {'class': 'pannable-image'}
        last_image = images[-1].find('img', attrs=attrs)
        image_url = last_image['data-src']
        SaveImage(image_url)
    except:
        print('exception in scrap')
        time.sleep(3)
        BackgroundImageExtractor(url)
#endregion


@background
def BackgroundSaveImage(url):
    try:
        url = urllib.parse.urljoin(url, urllib.parse.urlparse(url).path)
        name = 'images/' + basename(urllib.parse.urlparse(url).path)
        urllib.request.urlretrieve(url, name)
    except:
        print('exception in save')
        time.sleep(1)
        BackgroundSaveImage(url)

def ImageExtractor(url):
    try:
        HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})
        webpage = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, 'lxml')
        images = soup.find_all('div', class_=['c-remodal-gallery__main-img', 'js-gallery-main-img'])
        attrs = {'class': 'pannable-image'}
        last_image = images[-1].find('img', attrs=attrs)
        image_url = last_image['data-src']
        BackgroundSaveImage(image_url)
    except:
        print('exception in scrap')
        time.sleep(3)
        BackgroundImageExtractor(url)


def initializer(url):
    attrs = {'class': 'js-product-url'}
    urls = []
    
    HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    webpage = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, 'lxml')
    for a in soup.findAll('a', href=True, attrs=attrs):
        urls.append('https://www.digikala.com' + a['href'])
    
    print(url, len(urls))
    for url in urls:
        ImageExtractor(url)

def main():
    home_url = 'https://www.digikala.com/treasure-hunt/products/'
    product_urls = []
    print('app started...')
    #product_urls += initializer(home_url)
    Parallel(n_jobs=2)(delayed(initializer)(home_url + '?pageno=' + str(i) + '&sortby=4') for i in range(1, 48))

    

if __name__ == "__main__": main()