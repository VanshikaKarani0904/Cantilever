import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import time, random, re
import sqlite3

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def rating_to_number(rating_word):
    ratings = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    return ratings.get(rating_word, 0)

def get_soup(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "lxml")

books = []

for page in range(1, 6):   # scrape first 5 pages
    page_url = BASE_URL.format(page)
    print(f"Scraping {page_url}")
    soup = get_soup(page_url)

    for item in soup.find_all('article', class_='product_pod'):
        title = item.h3.a['title']

        price_text = item.find('p', class_='price_color').get_text(strip=True)
        price_match = re.search(r"[\d.]+", price_text)
        price = float(price_match.group()) if price_match else None

        rating_word = item.find('p', class_='star-rating')['class'][1]
        rating = rating_to_number(rating_word)

        relative_link = item.h3.a['href']
        detail_url = urljoin(page_url, relative_link)

        description = ""
        try:
            detail_soup = get_soup(detail_url)
            desc_heading = detail_soup.find('div', id='product_description')
            if desc_heading:
                description = desc_heading.find_next_sibling('p').get_text(strip=True)
        except Exception:
            pass

        books.append({
            'title': title,
            'price': price,
            'rating': rating,
            'detail_url': detail_url,
            'description': description
        })

    time.sleep(random.uniform(1, 2))  # pause between pages

# Save to Excel
df = pd.DataFrame(books)
df.to_excel("books_data.xlsx", index=False)
print("Saved data to books_data.xlsx")

# Save to SQLite
conn = sqlite3.connect("books.db")
df.to_sql("books", conn, if_exists="replace", index=False)
conn.close()
print("Saved data to books.db")
