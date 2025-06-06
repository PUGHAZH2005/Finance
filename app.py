from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse
import psycopg2
from datetime import datetime
import os

# ✅ Get DB URL from environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL environment variable is not set!")

# ✅ Convert 'postgresql://' to 'postgres://' for psycopg2 compatibility
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgres://", 1)

# ✅ Connect to PostgreSQL
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

# ✅ Create tables if they don't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS finance_data (
    id SERIAL PRIMARY KEY,
    date DATE,
    income NUMERIC,
    income_note TEXT,
    food NUMERIC,
    food_note TEXT,
    travel NUMERIC,
    travel_note TEXT,
    clothes NUMERIC,
    clothes_note TEXT,
    others NUMERIC,
    others_note TEXT
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS loan_debt (
    id SERIAL PRIMARY KEY,
    date DATE,
    name TEXT,
    amount NUMERIC,
    type TEXT,
    note TEXT,
    status TEXT
)
""")
conn.commit()

class FinanceHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode()
        params = urllib.parse.parse_qs(body)

        if self.path == '/save':
            date = params.get('date', [datetime.today().strftime('%Y-%m-%d')])[0]
            income = params.get('income', ['0'])[0]
            income_note = params.get('income_note', [''])[0]
            food = params.get('food', ['0'])[0]
            food_note = params.get('food_note', [''])[0]
            travel = params.get('travel', ['0'])[0]
            travel_note = params.get('travel_note', [''])[0]
            clothes = params.get('clothes', ['0'])[0]
            clothes_note = params.get('clothes_note', [''])[0]
            others = params.get('others', ['0'])[0]
            others_note = params.get('others_note', [''])[0]

            cur.execute("""
            INSERT INTO finance_data (date, income, income_note, food, food_note, travel, travel_note, clothes, clothes_note, others, others_note)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (date, income, income_note, food, food_note, travel, travel_note, clothes, clothes_note, others, others_note))
            conn.commit()

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Saved to DB')

        elif self.path == '/loan':
            date = params.get('date', [datetime.today().strftime('%Y-%m-%d')])[0]
            name = params.get('name', [''])[0]
            amount = params.get('amount', ['0'])[0]
            type_ = params.get('type', ['debt'])[0]
            note = params.get('note', [''])[0]
            status = params.get('status', ['open'])[0]

            cur.execute("""
            INSERT INTO loan_debt (date, name, amount, type, note, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (date, name, amount, type_, note, status))
            conn.commit()

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Loan/Debt Saved to DB')

        else:
            super().do_GET()

# ✅ Start server on correct port
PORT = int(os.environ.get("PORT", 8000))
print(f"🚀 Server running on port {PORT}")
HTTPServer(('0.0.0.0', PORT), FinanceHandler).serve_forever()
