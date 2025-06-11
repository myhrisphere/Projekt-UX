from flask import Flask, render_template, request, redirect, url_for, session
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_key'

CSV_FILE = 'products.csv'

def read_products():
    products = []
    today = datetime.today().date()
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            raw_expires = row['expires']
            expires = datetime.strptime(raw_expires, "%Y-%m-%d").date()
            delta = (expires - today).days
            
            days_left = f"{delta} dni" if delta >= 0 else "PO TERMINIE"
            urgency = 'red' if delta < 2 else 'yellow' if delta < 5 else 'green'

            products.append({
                'name': row['name'],
                'quantity': row.get('quantity', '1'),
                'notes': row.get('notes', ''),
                'expires': expires.strftime("%d.%m.%Y"),
                'raw_expires': raw_expires,
                'days_left': days_left,
                'urgency': urgency
            })
    return sorted(products, key=lambda p: 9999 if p['days_left'] == "PO TERMINIE" else int(p['days_left'].split()[0]))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['login'] and request.form['password'] == 'user':
            session['user'] = request.form['login']
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Nieprawidłowe dane logowania.")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', products=read_products(), user=session['user'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                request.form['name'],
                request.form['expires'],
                request.form.get('quantity', '1'),
                request.form.get('notes', '')
            ])
        return redirect(url_for('dashboard'))

    return render_template('add_product.html', user=session['user'])


@app.route('/delete', methods=['POST'])
def delete_product():
    target_name = request.form['name']
    target_exp = request.form['expires']
    rows = []
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [r for r in reader if not (r['name'] == target_name and r['expires'] == target_exp)]
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['name', 'expires', 'quantity', 'notes'])
        writer.writeheader()
        writer.writerows(rows)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    # app.run(debug=True) #disable comment for debug
    app.run(host='0.0.0.0', port=5000)