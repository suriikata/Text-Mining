from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import requests



def find_description(url):
    """ finds description on current page. returns url with description. """
    text = BeautifulSoup(requests.get(url).content, features = 'lxml')
    abstract = ""
    try:
        div_descript = text.find('div', text = 'Opis')
        abstract = div_descript.findNext().text
    except Exception as e:
        print(f'tezave pri iskanju opisa za {url}')

    print(abstract)
    return url, abstract

def get_driver():
    driver = Firefox(service=Service(executable_path=GeckoDriverManager().install()))
    driver.implicitly_wait(3)
    return driver

def scrape(i):
    # Acta Hydrotechnica
    dlib_url = 'https://www.dlib.si/results/?euapi=1&query=%27keywords%3dpoplave*%27&sortDir=ASC&sort=date&pageSize=25&frelation=Acta+hydrotechnica&flanguage=slv'
    driver = get_driver()
    driver.get(dlib_url)
    titles = driver.find_elements(By.CLASS_NAME, 'Naslov')
    title = titles[i]
    url = title.find_element(By.TAG_NAME, 'a')
    url = url.get_property('href')
    driver.get(url)
    return url


skropucalo = scrape(3)
find_description(skropucalo)
