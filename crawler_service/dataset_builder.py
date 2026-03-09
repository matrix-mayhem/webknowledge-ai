import pandas as pd
from crawler import crawl_page
from clean_data import clean_text


def build_dataset(url):

    paragraphs = crawl_page(url)

    df = clean_text(paragraphs)

    df.to_csv("rag_service/docs.csv", index=False)

    print("Dataset created with", len(df), "rows")