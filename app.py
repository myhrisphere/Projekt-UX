from flask import Flask, render_template, request, redirect, url_for, session
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret-key'

def read_products():
    products = []
    today = datetime.today().date()
    with open('products.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            expires = datetime.strptime(row['expires'], '%Y-%m-%d').date()
            delta = (expires - today).days
            days_left = f"{delta} dni" if delta >= 0 else "PO TERMINIE"
            urgency = 'red' if delta < 2 else 'yellow' if delta < 5 else 'green'
            products.append({
                'name': row['name'],
                'expires': expires.strftime("%d.%m.%Y"),
                'days_left': days_left,
                'quantity': row['quantity'],
                'notes': row['notes'],
                'urgency': urgency
            })
    return products

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        if login and password == "user":
            session['user'] = login
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Nieprawidłowe dane logowania.")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    products = read_products()
    products.sort(key=lambda p: 9999 if p['days_left'] == "PO TERMINIE" else int(p['days_left'].split()[0]))
    return render_template('dashboard.html', products=products, user=session['user'])

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        new_entry = {
            'name': request.form['name'],
            'expires': request.form['expires'],
            'quantity': request.form['quantity'],
            'notes': request.form.get('notes', '')
        }
        with open('products.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'expires', 'quantity', 'notes'])
            writer.writerow(new_entry)
        return redirect(url_for('dashboard'))
    return render_template('add_product.html')

@app.route('/delete', methods=['POST'])
def delete_product():
    name_to_delete = request.form['name']
    products = []
    with open('products.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['name'] != name_to_delete:
                products.append(row)

    with open('products.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'expires', 'quantity', 'notes'])
        writer.writeheader()
        writer.writerows(products)

    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
