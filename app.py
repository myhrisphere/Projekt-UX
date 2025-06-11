from flask import Flask, render_template, request, redirect, url_for, session

import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'this-is-our-extremely-secret-key' 


def read_products():
    products = []
    today = datetime.today().date()

    with open('products.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            expires = datetime.strptime(row['expires'], "%Y-%m-%d").date()
            delta = (expires - today).days

            if delta < 0:
                days_left = "PO TERMINIE"
            else:
                days_left = f"{delta} dni"

            if days_left == "PO TERMINIE":
                urgency = 'red'
            elif delta < 2:
                urgency = 'red'
            elif delta < 5:
                urgency = 'yellow'
            else:
                urgency = 'green'

            products.append({
                'name': row['name'],
                'expires': expires.strftime("%d.%m.%Y"),
                'days_left': days_left,
                'urgency': urgency,
                'quantity': row.get('quantity', '1'),
                'notes': row.get('notes', 'brak')
            })
    return products

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        if login and password == "user":  # placeholder logic
            session['user'] = login
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Nieprawidłowe dane logowania.")
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    products = read_products()
    sorted_products = sorted(
        products,
        key=lambda p: (9999 if p['days_left'] == "PO TERMINIE" else int(p['days_left'].split()[0]))
    )
    return render_template('dashboard.html', products=sorted_products, user=session['user'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
