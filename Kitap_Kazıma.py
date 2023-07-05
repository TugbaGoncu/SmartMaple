import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client['kitapyurdu']
collection = db['kitaplar']

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

base_url = 'https://www.kitapyurdu.com/'
search_query = 'python'
url = base_url + f'index.php?route=product/search&filter_name={search_query}'


driver.get(url)

time.sleep(2)


last_page_elem = driver.find_element(By.CLASS_NAME, "next")
last_page_url = last_page_elem.get_attribute("href")
last_page = int(last_page_url.split("page=")[-1].split("&")[0])


books = []

for page in range(1, last_page + 1):
    page_url = url + f"&sayfa={page}"
    driver.get(page_url)
    time.sleep(2)

    book_names = driver.find_elements(By.CLASS_NAME, "name")
    prices = driver.find_elements(By.CLASS_NAME, "price-new")
    writers = driver.find_elements(By.CLASS_NAME, "author")
    publishers = driver.find_elements(By.CLASS_NAME, "publisher")

    for i in range(len(book_names)):
        book = {
            'name': book_names[i].text,
            'price': prices[i].text,
            'writer': writers[i].text,
            'publisher': publishers[i].text
        }
        books.append(book)

collection.insert_many(books)
print(f"{len(books)} kitap MongoDB'ye eklendi.")

driver.quit()
