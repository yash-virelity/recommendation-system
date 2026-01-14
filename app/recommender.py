import numpy as np
import random
from sklearn.metrics.pairwise import cosine_similarity
from app.config import INTERACTION_WEIGHTS, TOP_N, BODYTYPE_FIT_MAP, UNDERTONE_TAG_MAP

class HybridRecommender:

    def __init__(self, users, products, vectors, interactions):
        self.users = users
        self.products = products.reset_index(drop=True)
        self.vectors = vectors
        self.interactions = interactions

    def recommend(self, user_id, exclude_products=None):
        exclude_products = exclude_products or []

        user_row = self.users[self.users["user_id"] == user_id]
        body_type = user_row["userBodyType"].iloc[0] if not user_row.empty else None
        undertone = user_row["underTone"].iloc[0] if not user_row.empty else None

        user_actions = self.interactions[
            self.interactions["user_id"] == user_id
        ]

        scores = np.zeros(self.vectors.shape[0])

        # --- Interaction-based scoring (same as before) ---
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

        # --- Body Type Boost ---
        if body_type in BODYTYPE_FIT_MAP:
            preferred_fits = BODYTYPE_FIT_MAP[body_type]
            for i, product in self.products.iterrows():
                if any(fit in product["fits"] for fit in preferred_fits):
                    scores[i] += 0.5

        # --- Undertone Boost ---
        if undertone in UNDERTONE_TAG_MAP:
            preferred_tags = UNDERTONE_TAG_MAP[undertone]
            for i, product in self.products.iterrows():
                if any(tag in product["tags"] for tag in preferred_tags):
                    scores[i] += 0.3

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
