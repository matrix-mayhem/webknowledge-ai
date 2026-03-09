import pandas as pd
import numpy as np


def clean_text(paragraphs):

    df = pd.DataFrame(paragraphs, columns=["text"])

    # remove duplicates
    df = df.drop_duplicates()

    # remove short text
    df["length"] = df["text"].apply(len)

    threshold = np.mean(df["length"])

    df = df[df["length"] > threshold]

    df = df.drop(columns=["length"])

    return df