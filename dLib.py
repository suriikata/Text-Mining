from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
from PDF import create_txt
import requests


def find_description(url):
    text = BeautifulSoup(requests.get(url).content, features = 'lxml')
    abstract = ""
    try:
        div_descript = text.find('div', text = 'Opis')
        abstract = div_descript.findNext().text
        create_txt([abstract], 'dLib')
        print(abstract)
    except Exception as e:
        print(f'tezave pri iskanju opisa za {url}')

    return url, abstract

def get_driver():
    driver = Firefox(service=Service(executable_path=GeckoDriverManager().install()))
    driver.implicitly_wait(3)
    return driver

def scrape(url):
    driver = get_driver()
    driver.get(url)
    titles = driver.find_elements(By.CLASS_NAME, 'Naslov')
    n = len(titles)
    for i in range(n):
        titles = driver.find_elements(By.CLASS_NAME, 'Naslov')
        title = titles[i]
        url = title.find_element(By.TAG_NAME, 'a')
        url = url.get_property('href')
        find_description(url)


# Gradbeni vestnik (2) & Acta hydrotechnica (7)
dlib_urls = ['https://www.dlib.si/results/?euapi=1&query=%27keywords%3dpoplave%2c+gradbeni+vestnik*%27&sortDir=ASC&sort=date&pageSize=25',
            'https://www.dlib.si/results/?euapi=1&query=%27keywords%3dpoplave*%27&sortDir=ASC&sort=date&pageSize=25&frelation=Acta+hydrotechnica&flanguage=slv']

for url in dlib_urls:
    print(f'\n\nzacenjam z {url} \n\n')
    scrape(url)
