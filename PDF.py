import random
from os import listdir
from pypdf import PdfReader
from re import finditer
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import requests

def find_all_indexes(word, text):
    indexes = []
    for match in finditer(word, text):
        indexes.append(match.start())

    return indexes

def get_abstract(text):
    start_indexes = find_all_indexes('POVZETEK', text)
    end_indexes = find_all_indexes('ABSTRACT', text)

    abstracts = []
    for start_index, end_index in zip(start_indexes, end_indexes):
        abstract_start = start_index + len('POVZETEK')
        abstract_end = end_index
        abstract = text[abstract_start:abstract_end].rstrip()
        if 'poplav' in abstract:
            abstracts.append(abstract)
    """
    for a in abstracts:
        print(a)
    """
    return abstracts

def create_txt(abstracts, prefix):
    rand = random.randint(0, 10000)
    for a in abstracts:
        filename = f'output/{prefix}_{rand}.txt'
        print(f'\tsaving abstract to {filename}')
        with open(filename, 'wb') as f:
            f.write(a.encode('utf-8'))


def get_inputs():
    paths = []
    pdfs = listdir('slovenski_vodar')
    for pdf in pdfs:
        paths.append(f'slovenski_vodar/{pdf}')
    return paths

def get_driver():
    driver = Firefox(service=Service(executable_path=GeckoDriverManager().install()))
    driver.implicitly_wait(3)
    return driver

def download(url, local_path):
    response = requests.get(url)
    with open(local_path, 'wb') as f:
        f.write(response.content)


def scrape():
    sv_url = "http://www.drustvo-vodarjev.si/slovenski-vodar/"
    driver = get_driver()
    driver.get(sv_url)
    down_links = driver.find_elements(By.CLASS_NAME, 'filename')
    n = len(down_links)
    for i in range(n):
        down_links = driver.find_elements(By.CLASS_NAME, 'filename')
        down_link = down_links[i]
        url = down_link.find_element(By.TAG_NAME, 'a')
        url = url.get_property('href')
        filename = url.split('/')[-1]
        print(f'i={i} Trying to save {url} to filename {filename}')
        download(url, f'slovenski_vodar/{filename}')

#scrape()

if __name__ == '__main__':
    journals = get_inputs()

    for journal in journals:
        reader = PdfReader(journal)
        text = ""

        for page in reader.pages:
            text += page.extract_text() + "\n"
        print(f'extracting abstracts from {journal}')
        poganjavcek = get_abstract(text)
        create_txt(poganjavcek, "SV")



