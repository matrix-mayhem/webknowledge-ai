import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import certifi

def crawl_url(url):
    response = requests.get(url, verify=certifi.where())
    soup = BeautifulSoup(response.text,"html.parser")
    paragraphs = [p.text for p in soup.find_all("p")]
    df = pd.DataFrame(paragraphs,columns=['content'])

    #data cleaning
    df["length"] = df["content"].apply(len)

    threshold = np.mean(df["length"])

    df = df[df["length"] > threshold]

    return df
