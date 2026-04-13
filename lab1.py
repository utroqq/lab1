import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin


def count_all_lego():
    base_url = 'https://www.detmir.ru/catalog/index/name/lego/'
    domain = "https://www.detmir.ru"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    total_discounted_count = 0
    page_number = 1

    with open("lego_discounts.txt", "w", encoding="utf-8") as file:

        while True:
            url = f"{base_url}page/{page_number}/"

            try:
                response = requests.get(url, headers=headers, timeout=10)

                if response.status_code != 200:
                    break

                soup = BeautifulSoup(response.text, "html.parser")

                items = soup.find_all("a", href=True)

                found_on_page = 0

                for a in items:
                    href = a["href"]
                    if "/product/" not in href:
                        continue
                    parent = a.find_parent()
                    if not parent:
                        continue
                    discount_tag = parent.find('div', attrs={'data-testid': 'labelDiscount'})
                    if not discount_tag:
                        continue
                    raw_text = discount_tag.get_text()
                    digits = "".join(filter(str.isdigit, raw_text))
                    if not digits:
                        continue
                    discount = int(digits)
                    if discount >= 30:
                        title = a.get_text(strip=True)
                        link = urljoin(domain, href)
                        line = f"{title} | -{discount}% | {link}\n"
                        file.write(line)
                        total_discounted_count += 1
                        found_on_page += 1
                print(f"Страница {page_number}: найдено {found_on_page}")
                page_number += 1
                if page_number > 20:
                    break
                time.sleep(1)
            except Exception as e:
                print(f"Ошибка: {e}")
                break
if __name__ == "__main__":
    count_all_lego()