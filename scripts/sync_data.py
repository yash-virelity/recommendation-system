import requests
import pandas as pd
import os

BASE_URL = "http://localhost:8080/api"
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# ------------------ HELPERS ------------------

def load_existing_csv(path):
    return pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()

def save_csv(df, path):
    df.to_csv(path, index=False)

# ------------------ USERS ------------------

def sync_users():
    resp = requests.get(f"{BASE_URL}/users")
    resp.raise_for_status()
    users = resp.json() # Your JSON shows this is a direct list []

    rows = []
    for u in users:
        rows.append({
            "user_id": u.get("_id"), # Use _id as the primary key
            "email": u.get("email"),
            "gender": u.get("gender"),
            "age_range": u.get("age_range"),
            "fashion_preferences": u.get("fashion_preferences", []),
            "onboarding_completed": u.get("onboarding_completed"),
            "created_at": u.get("created_at"),
            "updated_at": u.get("updated_at")
        })

    new_df = pd.DataFrame(rows)
    old_df = load_existing_csv(f"{DATA_DIR}/users.csv")
    final_df = pd.concat([old_df, new_df]).drop_duplicates(subset=["user_id"], keep="last")
    save_csv(final_df, f"{DATA_DIR}/users.csv")
    print(f"✅ Users synced: {len(final_df)}")

# ------------------ PRODUCTS ------------------

def sync_products():
    resp = requests.get(f"{BASE_URL}/products")
    resp.raise_for_status()
    products = resp.json() # Your JSON shows this is a direct list []

    rows = []
    for p in products:
        # Fixed: Handle the nested price and category objects safely
        price_obj = p.get("price") or {}
        cat_obj = p.get("category") or {}
        brand_obj = p.get("brand") or {}

        rows.append({
            "product_id": p.get("_id"),
            "name": p.get("name"),
            "description": p.get("description"),
            "price": price_obj.get("$numberDecimal"), 
            "currency": p.get("currency"),
            "category": cat_obj.get("name"),
            "brand": brand_obj.get("name"),
            "stock": p.get("stock"),
            "is_active": p.get("is_active"),
            "created_at": p.get("created_at"),
            "updated_at": p.get("updated_at")
        })

    new_df = pd.DataFrame(rows)
    old_df = load_existing_csv(f"{DATA_DIR}/products.csv")
    final_df = pd.concat([old_df, new_df]).drop_duplicates(subset=["product_id"], keep="last")
    save_csv(final_df, f"{DATA_DIR}/products.csv")
    print(f"✅ Products synced: {len(final_df)}")

# ------------------ INTERACTIONS ------------------

def sync_interactions():
    resp = requests.get(f"{BASE_URL}/users/preferences")
    resp.raise_for_status()
    
    # FIXED: Accessing the nested 'preferences' array based on your JSON snippet
    data_payload = resp.json()
    interactions = data_payload.get("data", {}).get("preferences", [])

    rows = []
    for i in interactions:
        # Accessing nested user and product IDs
        user_info = i.get("user") or {}
        prod_info = i.get("product") or {}
        
        rows.append({
            "interaction_id": i.get("_id"),
            "user_id": user_info.get("_id"),
            "product_id": prod_info.get("_id"),
            "action": i.get("action"),
            "timestamp": i.get("timestamp")
        })

    new_df = pd.DataFrame(rows)
    old_df = load_existing_csv(f"{DATA_DIR}/interactions.csv")
    
    # Using interaction_id or a combo of user/product/timestamp to prevent duplicates
    final_df = pd.concat([old_df, new_df]).drop_duplicates(
        subset=["user_id", "product_id", "timestamp"], 
        keep="last"
    )
    save_csv(final_df, f"{DATA_DIR}/interactions.csv")
    print(f"✅ Interactions synced: {len(final_df)}")

if __name__ == "__main__":
    sync_users()
    sync_products()
    sync_interactions()