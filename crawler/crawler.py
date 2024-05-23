from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from uuid import uuid4
import os

def create_directory():
    directory = str(uuid4())
    os.mkdir(directory)
    return directory


def crawl_page(url, depth):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    directory = create_directory()
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    pic = f'{directory}/{directory}.png' # not the best name, but it's unique
    driver.save_screenshot(pic) 
    elems = driver.find_elements(By.XPATH, "//a[@href]")
    links_and_pics = [(url, pic)]
    urls = [elem.get_attribute("href") for elem in elems[:depth]]
    for url in urls:
        driver.get(url)
        unique_id = str(uuid4())
        pic = f'{directory}/{unique_id}.png'
        driver.save_screenshot(pic)
        links_and_pics.append((url, pic))
    driver.close()
    return (directory, links_and_pics)
