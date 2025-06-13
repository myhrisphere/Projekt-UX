# 📦 FreshAlert

FreshAlert is a simple Flask web app for managing food items and tracking their expiration dates. Users can log in, add/delete products stored in a CSV file, and view details in a popup card.

You can check the app out at [Live Demo](https://projekt-ux-production.up.railway.app) with these credentials:
  *  Login: user
  *  Password: user

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Install & Setup
```bash
git clone https://github.com/myhrisphere/Projekt-UX.git
cd Projekt-UX
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Run
```bash
set FLASK_APP=app.py
set FLASK_ENV=development  # or export on macOS/Linux
flask run
```
Visit [http://localhost:5000](http://localhost:5000) and log in (password = `"user"`). 

---

## 🔧 Project Structure

```
Projekt-UX/
├── app.py
├── products.csv
├── requirements.txt
├── static/
│   ├── style.css
│   ├── script.js
│   ├── logo.png
│   └── logo-img-only.png
└── templates/
    ├── login.html
    ├── dashboard.html
    └── add_product.html
```

---

## 🛠️ app.py

This is the main Flask app with routes:

- `/` — login (POST)
- `/dashboard` — view product list (GET)
- `/add` — add product form (GET/POST)
- `/delete` — delete a product (POST)
- `/logout` — clear session (GET)

Products are read/written from `products.csv` using Python's CSV library.

---

## 🗂️ products.csv

CSV columns:

```
name,expires,quantity,notes
Milk,2025-06-12,1,"Save half bottle for cake."
```

- `expires` must be `YYYY‑MM‑DD`
- `quantity` numeric, default `1`
- `notes` free text

---

## 🧩 Templates

### login.html
A login form with `login-btn`. On success, redirects to dashboard.

### dashboard.html
Main UI showing:
- Top 4 soonest-expiring items
- Full fridge grid (4 columns)
- Click a product to open a **popup card** showing *name, expiration, quantity, notes*
- Delete via trash icon, form posts to `/delete`

### add_product.html
Form for adding new product:
- Fields: name, date, quantity, notes
- Submit POST to `/add`

---

## 🎨 Static Assets

### style.css
Contains:
- Layout, colors, responsive stylesheet
- Popup card style: position `absolute`, hidden by default with `hidden` class

### script.js
Handles popup logic on dashboard:
- `togglePopup(id)` shows/hides card
- Positions card next to clicked product
- Closes popup on outside click or close icon

### logo & favicon
Add this in `<head>` of HTML pages to set favicon:

```html
<link rel="icon" href="{{ url_for('static', filename='logo-img-only.png') }}">
```

---

## ✅ Usage Workflow

1. User logs in (any username / password = "user")
2. Redirect to `/dashboard`
3. Click "+ DODAJ PRODUKT" → opens `/add`
4. Fill form → POST `/add` → append CSV → redirect back
5. On dashboard: click product → popup appears with full info
6. Close popup with × or click outside
7. Delete product → form posts to `/delete`, updates CSV, reloads

---

## 📌 Technical Details

- **Flask** for web framework  
- **Session** to enforce login  
- CSV-based storage (no DB) for simplicity  
- **Jinja2** to inject products and build grid  
- Popup is handled client-side (JS + CSS)

---

## 📝 License
## License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/).

You are free to:
- Use and modify the code for **personal, non-commercial purposes**
- Share your modifications with attribution

You are **not allowed** to:
- Use this project or its derivatives for **commercial purposes**
- Sell or include this in paid products or services

For commercial use inquiries, please contact the author.
