# Recommendation System

This service provides **real-time personalized product recommendations** using a **hybrid content-based approach** combined with **user interaction signals**.
It is designed to be simple, explainable, and scalable for incremental data growth.

---

## How the Recommendation Works

- Product metadata (tags, category, subcategory, brand, fit) is converted into **TF-IDF vectors**.
- **Cosine similarity** is used to measure similarity between products.
- User interactions are converted into **weighted signals** and applied to similar products.
- The system scores all products and returns the **top-N highest scoring items**.

---

## Installation and Testing Guide:

- Clone the repository
- create a virtual environment - `python -m venv venv`
- activate the virtual environment - `venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`
- Run the application: `python main.py`
- Test the API: `http://localhost:8000/recommend/:userId`
  Eg: `http://localhost:8000/recommend/user_3`

## Cold Start Handling

- New users with no interactions receive:
  - Random active products or popular items
- New products are recommended based on:
  - Content similarity to existing products
- Partial onboarding data still improves initial relevance.

---

## Repetition Control (Freshness)

- Recent recommendations are cached per user for a short TTL.
- On repeated requests:

  - Previously shown products are partially excluded
  - Order is shuffled
  - New products are injected

- This avoids the system feeling static or repetitive.

---

## Factors Considered for Recommendations

### Product Factors

- Tags (e.g., streetwear, formal, casual)
- Category and subcategory
- Brand
- Fit and style keywords

### User Factors

- Likes, views, purchases, dislikes
- Strength of interaction (purchase > like > view)
- Negative feedback actively penalizes similar products

### System Factors

- Product availability (active products only)
- Short-term cache to avoid repetitive recommendations

---

## Interaction Weighting Logic

- View → low positive signal
- Like → strong positive signal
- Purchase → strongest positive signal
- Dislike → strong negative signal

Negative interactions reduce the likelihood of similar products appearing.

---

## Edge Cases Handled

- Users with no interactions
- Products referenced in interactions but no longer active
- Rapid repeated API calls
- Disliked products suppressing entire similarity clusters
- Missing or malformed list fields in CSV data

---

## Incremental Data Handling

- New users and interactions automatically influence scoring without code changes.
- The system recalculates recommendations dynamically using the latest interaction data.
- For growth:

  - Product vectors can be retrained periodically
  - Cache can be upgraded to Redis
  - Offline batch processing can be introduced

---
