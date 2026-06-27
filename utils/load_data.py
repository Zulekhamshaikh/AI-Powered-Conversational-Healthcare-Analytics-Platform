import pandas as pd

def load_data():
    df = pd.read_csv("data/cleaned_healthcare.csv")
    return df