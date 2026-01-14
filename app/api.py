from fastapi import FastAPI
from app.data_loader import load_data
from app.preprocessing import parse_list_columns
from app.feature_engineering import build_product_vectors
from app.recommender import HybridRecommender
from app.cache import RecommendationCache

app = FastAPI(title="Recommendation Service")

users, products, interactions = load_data()

products = parse_list_columns(products, ["tags", "sizes", "fits"])

vectors = build_product_vectors(products)

recommender = HybridRecommender(
    users=users,
    products=products,
    vectors=vectors,
    interactions=interactions
)

cache = RecommendationCache(ttl_seconds=10)

@app.get("/recommend/{user_id}")
def recommend(user_id: str):
    cached = cache.get(user_id)

    if cached:
        new_recs = recommender.recommend(
            user_id,
            exclude_products=cached
        )
        final =  new_recs[:12] + cached[:3]
    else:
        final = recommender.recommend(user_id)

    cache.set(user_id, final)

    return {
        "user_id": user_id,
        "recommendations": final
    }
