import numpy as np
import random
from sklearn.metrics.pairwise import cosine_similarity
from app.config import INTERACTION_WEIGHTS, TOP_N

class HybridRecommender:

    def __init__(self, products, vectors, interactions):
        self.products = products.reset_index(drop=True)
        self.vectors = vectors
        self.interactions = interactions

    def recommend(self, user_id, exclude_products=None):
        exclude_products = exclude_products or []

        user_actions = self.interactions[
            self.interactions["user_id"] == user_id
        ]

        scores = np.zeros(self.vectors.shape[0])

        if user_actions.empty:
            candidates = self.products[
                ~self.products["product_id"].isin(exclude_products)
            ]
            return candidates.sample(TOP_N)["product_id"].tolist()

        for _, row in user_actions.iterrows():
            try:
                idx = self.products[
                    self.products["product_id"] == row["product_id"]
                ].index[0]
            except:
                continue

            weight = INTERACTION_WEIGHTS.get(row["action"], 0)
            similarity = cosine_similarity(
                self.vectors[idx],
                self.vectors
            )[0]

            scores += weight * similarity

        ranked_indices = scores.argsort()[::-1]

        recommendations = []
        for idx in ranked_indices:
            pid = self.products.iloc[idx]["product_id"]
            if pid not in exclude_products:
                recommendations.append(pid)
            if len(recommendations) >= TOP_N:
                break

        random.shuffle(recommendations)
        return recommendations
