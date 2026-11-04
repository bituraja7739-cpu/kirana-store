import json
import urllib.request
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_credentials():
    url = os.environ.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_KEY", "")
    cfg_file = os.path.join(BASE_DIR, "supabase_config.json")
    if os.path.exists(cfg_file):
        try:
            with open(cfg_file, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                url = url or cfg.get("SUPABASE_URL", "")
                key = key or cfg.get("SUPABASE_KEY", "")
        except Exception:
            pass
    return url, key

SUPABASE_URL, SUPABASE_KEY = load_credentials()

def upload_items():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Supabase credentials not found!")
        return False

    db_file = os.path.join(BASE_DIR, "kirana_db.json")
    with open(db_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = data.get("items", [])
    print(f"Preparing to upload {len(items)} items to Supabase...")

    rows = []
    for it in items:
        rows.append({
            "id": str(it.get("id")),
            "name": it.get("name"),
            "category": it.get("category", "General"),
            "unit": it.get("unit", "pcs"),
            "buy_price": float(it.get("buyPrice", 0)),
            "sell_price": float(it.get("sellPrice", 0)),
            "stock": float(it.get("stock", 0)),
            "min_stock": float(it.get("minStock", 5)),
            "updated_at": int(it.get("updatedAt", 0))
        })

    url = f"{SUPABASE_URL}/rest/v1/items"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }

    req = urllib.request.Request(url, data=json.dumps(rows).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"Successfully uploaded {len(rows)} items! Status: {resp.getcode()}")
            return True
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
        return False
    except Exception as ex:
        print(f"Error: {ex}")
        return False

if __name__ == "__main__":
    upload_items()
