# 🏠 Zillow.com Tracker PRO

**Zillow.com Tracker PRO** is a powerful real estate market tracking dashboard that scrapes and analyzes listing data from Zillow, then visualizes key insights like price trends, average home prices, and total active listings in a clean, responsive web interface.

---

## 🚀 Features

- 📈 **Real-Time Price Trends**  
  View historical average price trends with beautiful, interactive charts.

- 💰 **Market Insights**  
  See average listing prices and new listings for the week.

- 🧮 **Listing Analytics**  
  Instantly check total properties scraped and analyzed.

- 🎨 **Modern UI**  
  Responsive, animated, and visually appealing dashboard built with React and Recharts.

---

## 🧩 Tech Stack

| Frontend    | Backend       | Data Layer      | Styling         |
|-------------|---------------|------------------|------------------|
| React.js    | Flask (Python) | Zillow Scraper (Python) | CSS3, Recharts |

---

## 📊 Screenshots

<img src="https://via.placeholder.com/800x400?text=Dashboard+Overview" alt="Dashboard UI" />

---

## 📦 Project Structure

```
zillow-tracker-pro/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── Dashboard.jsx
│   │   └── Dashboard.css
│   └── public/
├── backend_api/                 # Python backend
│   ├── app.py
│   ├── auth.py
├── database/                 # Python backend
│   ├── connection.py
│   ├── models.py
│   ├── operations.py
├── scraper/                 # Python backend
│   ├── constants.py
│   ├── main.py
│   ├── zillow.py
└── README.md
```

---

## ⚙️ Getting Started

### 1️⃣ Prerequisites

- Node.js & npm
- Python 3.9+
- pipenv or virtualenv

### 2️⃣ Clone the Repo

```bash
git clone https://github.com/ShujaatAli88/Real-Estate-Full-Stack-Trend-Tracker.git
cd Real-Estate-Full-Stack-Trend-Tracker
```

### 3️⃣ Install & Run Backend

```bash
cd server
pip install -r requirements.txt
python app.py
```

### 4️⃣ Install & Run Frontend

```bash
cd client
npm install
npm start
```

> Frontend will run on `http://localhost:3000` and talk to Flask on `http://localhost:5000`.

---

## 🔌 API Endpoints

| Endpoint                      | Description                    |
|------------------------------|--------------------------------|
| `/api/price-trends`          | Returns historical price data  |
| `/api/average-price`         | Returns average price          |
| `/api/total-listings`        | Returns number of listings     |

---

## 📈 Chart Features

- Tooltips with currency formatting
- Trendline with gradient fill
- Hover points & animation
- Mobile-responsive with `Recharts`

---

## 🌐 Deployment Suggestions

- Frontend: Vercel, Netlify, or GitHub Pages
- Backend: Railway, Render, or Heroku
- Dockerize for full CI/CD deployment

---

## 🧠 Future Improvements

- 🔍 Filter by city/zipcode
- 📅 Date range selector
- 🔄 Auto-refresh crawler
- 📤 Export data to CSV/Excel
- 📱 PWA support

---

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first to discuss.

---

## ✨ Author

Made with ❤️ by Shujaat Ali