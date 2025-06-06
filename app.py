from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse
import csv
from datetime import datetime
import os

class FinanceHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode()
        params = urllib.parse.parse_qs(body)

        # 🚀 Handle main finance data
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

            row = [
                date, income, income_note,
                food, food_note,
                travel, travel_note,
                clothes, clothes_note,
                others, others_note
            ]

            file_exists = os.path.isfile('finance_data.csv')
            with open('finance_data.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow([
                        'Date', 'Income', 'IncomeNote',
                        'Food', 'FoodNote',
                        'Travel', 'TravelNote',
                        'Clothes', 'ClothesNote',
                        'Others', 'OthersNote'
                    ])
                writer.writerow(row)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Saved')

        # 💳 Handle loan/debt entries
        elif self.path == '/loan':
            date = params.get('date', [datetime.today().strftime('%Y-%m-%d')])[0]
            name = params.get('name', [''])[0]
            amount = params.get('amount', ['0'])[0]
            type_ = params.get('type', ['debt'])[0]
            note = params.get('note', [''])[0]
            status = params.get('status', ['open'])[0]

            row = [date, name, amount, type_, note, status]

            file_exists = os.path.isfile('loan_debt.csv')
            with open('loan_debt.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(['Date', 'Name', 'Amount', 'Type', 'Note', 'Status'])
                writer.writerow(row)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Loan/Debt Saved')

        else:
            self.handle_static()

    def handle_static(self):
        # 📁 Serve loan_debt.csv if requested explicitly
        if self.path == "/loan_debt.csv" and os.path.exists("loan_debt.csv"):
            self.send_response(200)
            self.send_header("Content-Type", "text/csv")
            self.end_headers()
            with open("loan_debt.csv", "rb") as f:
                self.wfile.write(f.read())
        # 📁 Serve finance_data.csv if requested explicitly
        elif self.path == "/finance_data.csv" and os.path.exists("finance_data.csv"):
            self.send_response(200)
            self.send_header("Content-Type", "text/csv")
            self.end_headers()
            with open("finance_data.csv", "rb") as f:
                self.wfile.write(f.read())
        else:
            # 🌐 Serve index.html, charts, and other static files
            super().do_GET()

# ✅ Run server
PORT = 8000
print(f"🚀 Server running at http://localhost:{PORT}")
HTTPServer(('localhost', PORT), FinanceHandler).serve_forever()
