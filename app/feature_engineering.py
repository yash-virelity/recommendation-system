from sklearn.feature_extraction.text import TfidfVectorizer

def build_product_vectors(products):
    products["combined"] = (
        products["tags"].astype(str) + " " +
        products["category"] + " " +
        products["subcategory"] + " " +
        products["brand"]
    )

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(products["combined"])

    return vectors
