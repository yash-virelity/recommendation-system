import pandas as pd

def load_data():
    users = pd.read_csv("data/users.csv")
    products = pd.read_csv("data/products.csv")
    interactions = pd.read_csv("data/interactions.csv")
    return users, products, interactions
