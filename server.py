import http.server
import socketserver
import webbrowser
import socket
import json
import os
import sys

PORT = int(os.environ.get("PORT", 8080))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "kirana_db.json")

# Default seed data if database file does not exist
DEFAULT_ITEMS = [
    { "id": "1", "name": "Sugar (Cheeni)", "category": "Grains & Pulses", "unit": "kg", "buyPrice": 40, "sellPrice": 44, "stock": 85, "minStock": 15 },
    { "id": "2", "name": "Chana Dal", "category": "Grains & Pulses", "unit": "kg", "buyPrice": 75, "sellPrice": 88, "stock": 42, "minStock": 10 },
    { "id": "3", "name": "Toor Dal (Arhar)", "category": "Grains & Pulses", "unit": "kg", "buyPrice": 130, "sellPrice": 150, "stock": 28, "minStock": 8 },
    { "id": "4", "name": "Mustard Oil 1L (Sarso)", "category": "Oils & Ghee", "unit": "pcs", "buyPrice": 135, "sellPrice": 155, "stock": 24, "minStock": 6 },
    { "id": "5", "name": "Fortune Refined Oil 1L", "category": "Oils & Ghee", "unit": "pcs", "buyPrice": 115, "sellPrice": 130, "stock": 18, "minStock": 5 },
    { "id": "6", "name": "Basmati Rice", "category": "Grains & Pulses", "unit": "kg", "buyPrice": 85, "sellPrice": 105, "stock": 60, "minStock": 15 },
    { "id": "7", "name": "Tata Salt 1kg", "category": "General", "unit": "pcs", "buyPrice": 24, "sellPrice": 28, "stock": 50, "minStock": 10 },
    { "id": "8", "name": "Red Chilli Powder", "category": "Spices", "unit": "kg", "buyPrice": 240, "sellPrice": 320, "stock": 12, "minStock": 3 },
    { "id": "9", "name": "Turmeric Powder (Haldi)", "category": "Spices", "unit": "kg", "buyPrice": 200, "sellPrice": 260, "stock": 14, "minStock": 3 },
    { "id": "10", "name": "Coriander Powder (Dhaniya)", "category": "Spices", "unit": "kg", "buyPrice": 180, "sellPrice": 230, "stock": 9, "minStock": 3 },
    { "id": "11", "name": "Parle-G Biscuit ₹10", "category": "Snacks & Biscuits", "unit": "pcs", "buyPrice": 8.5, "sellPrice": 10, "stock": 75, "minStock": 15 },
    { "id": "12", "name": "Lux Soap Bar", "category": "Soaps & Detergents", "unit": "pcs", "buyPrice": 28, "sellPrice": 35, "stock": 32, "minStock": 8 },
    { "id": "13", "name": "Surf Excel 1kg", "category": "Soaps & Detergents", "unit": "pcs", "buyPrice": 125, "sellPrice": 140, "stock": 16, "minStock": 4 },
    { "id": "14", "name": "Taj Mahal Tea 250g", "category": "General", "unit": "pcs", "buyPrice": 95, "sellPrice": 120, "stock": 22, "minStock": 5 }
]

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {DB_FILE}: {e}")
    initial_db = {
        "shopName": "Grocery & Kirana Store",
        "phone": "9876543210",
        "address": "Main Market, Shop #12",
        "items": DEFAULT_ITEMS,
        "sales": [],
        "lastUpdated": ""
    }
    save_db(initial_db)
    return initial_db

def save_db(data):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving {DB_FILE}: {e}")

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class KiranaRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        # Enable CORS and caching rules
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/data":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            db_data = load_db()
            self.wfile.write(json.dumps(db_data).encode("utf-8"))
            return
        elif self.path == "/sw.js":
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript")
            self.send_header("Service-Worker-Allowed", "/")
            self.end_headers()
            sw_path = os.path.join(BASE_DIR, "sw.js")
            with open(sw_path, "rb") as f:
                self.wfile.write(f.read())
            return
        elif self.path == "/manifest.json":
            self.send_response(200)
            self.send_header("Content-Type", "application/manifest+json")
            self.end_headers()
            manifest_path = os.path.join(BASE_DIR, "manifest.json")
            with open(manifest_path, "rb") as f:
                self.wfile.write(f.read())
            return

        # Default static file handler
        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/sync":
            content_length = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_length)
            try:
                incoming_data = json.loads(post_body.decode('utf-8'))
                current_db = load_db()

                # Merge items: update rates & stocks
                laptop_items_map = {item['id']: item for item in current_db.get('items', [])}
                mobile_items = incoming_data.get('items', [])
                for m_item in mobile_items:
                    m_id = m_item.get('id')
                    if m_id in laptop_items_map:
                        # Update fields
                        laptop_items_map[m_id].update(m_item)
                    else:
                        laptop_items_map[m_id] = m_item
                current_db['items'] = list(laptop_items_map.values())

                # Merge sales: add non-duplicate sales by billNo
                existing_bills = {s.get('billNo') for s in current_db.get('sales', [])}
                mobile_sales = incoming_data.get('sales', [])
                for m_sale in mobile_sales:
                    if m_sale.get('billNo') not in existing_bills:
                        current_db['sales'].insert(0, m_sale)
                        existing_bills.add(m_sale.get('billNo'))

                # Update shop profile if provided
                if incoming_data.get('shopName'):
                    current_db['shopName'] = incoming_data['shopName']
                if incoming_data.get('phone'):
                    current_db['phone'] = incoming_data['phone']
                if incoming_data.get('address'):
                    current_db['address'] = incoming_data['address']

                save_db(current_db)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                response = {
                    "status": "success",
                    "message": "Data synchronized successfully with Laptop!",
                    "db": current_db
                }
                self.wfile.write(json.dumps(response).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

def run_server():
    os.chdir(BASE_DIR)
    local_ip = get_local_ip()
    mobile_url = f"http://{local_ip}:{PORT}"
    local_url = f"http://localhost:{PORT}"

    print("=" * 65)
    print("      KiranaPro Server with Mobile Offline-Sync")
    print("=" * 65)
    print(f"[*] Computer Link     : {local_url}")
    print(f"[*] Mobile Phone Link : {mobile_url}")
    print("=" * 65)
    print("[INFO] HOW OFFLINE ON MOBILE WORKS:")
    print("1. Open the Mobile Link on your phone (Chrome/Safari).")
    print("2. Tap 'Add to Home Screen' or 'Install App'.")
    print("3. NOW EVEN IF THIS LAPTOP IS COMPLETELY TURNED OFF:")
    print("   - The app will ALWAYS open on your mobile phone!")
    print("   - Full item search, rates, and selling work 100% offline.")
    print("4. Whenever you turn this laptop ON again:")
    print("   - Just tap 'Sync with Laptop' on mobile to update everything!")
    print("=" * 65)
    print("Press Ctrl + C to stop server.\n")

    # Automatically open local browser if running on local desktop
    if "RENDER" not in os.environ and sys.platform.startswith("win"):
        try:
            webbrowser.open(local_url)
        except Exception:
            pass

    # Allow address reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), KiranaRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    run_server()
