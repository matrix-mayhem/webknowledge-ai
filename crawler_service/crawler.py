import requests
from bs4 import BeautifulSoup


def crawl_page(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    paragraphs = []

    for p in soup.find_all("p"):
        text = p.get_text().strip()

        if text:
            paragraphs.append(text)

    return paragraphs