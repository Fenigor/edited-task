import selenium

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def crawl_page(url, depth):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.save_screenshot('foo.png')
    elems = driver.find_elements(By.XPATH, "//a[@href]")
    urls = [elem.get_attribute("href") for elem in elems[:depth]]
    for i, url in enumerate(urls):
        print(url, i)
        driver.get(url)
        driver.save_screenshot(f'{i}/foo{i}.png')
    driver.close()


crawl_page('https://edited.com', 2)
