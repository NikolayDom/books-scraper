import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_books(start_url):
    url = start_url
    all_books = []
    page_num = 1

    print(f"Начинаю сбор данных с {start_url}")
    
    while True:
        print(f"  Обрабатываю страницу {page_num}: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"  Ошибка при загрузке страницы: {e}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        book_blocks = soup.find_all("article", class_="product_pod")

        for block in book_blocks:
            title = block.find("h3").find("a")['title']
            
            price = block.find("p", class_="price_color").text
            
            img_link = block.find("img")['src']
            full_img_link = "https://books.toscrape.com/" + img_link
            
            all_books.append({
                "название": title,
                "цена": price,
                "ссылка_на_картинку": full_img_link
            })

        next_button = soup.select_one('li.next a')
        if next_button:
            next_page = next_button.get("href")
            if next_page.startswith("catalogue"):
                url = "https://books.toscrape.com/" + next_page
            else:
                url = "https://books.toscrape.com/catalogue/" + next_page
            page_num += 1
        else:
            print("  Достигнут конец каталога.")
            break

    print(f"Собрано книг: {len(all_books)}")
    return all_books

def save_to_json(data, filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(project_dir, "data")
    
    os.makedirs(data_dir, exist_ok=True)
    
    filepath = os.path.join(data_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    print(f"Файл сохранён: {filepath}")

if __name__ == "__main__":
    books = scrape_books("https://books.toscrape.com/")
    save_to_json(books, "books.json")