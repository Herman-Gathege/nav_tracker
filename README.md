# 🧮 ICM NAV Tracker – Crypto Index Valuation System

A full-stack app to calculate, store, and visualize the **Net Asset Value (NAV)** of a crypto index product based on real wallet balances from **Ethereum** and **Solana**.

Built with **Flask (Python)** for the backend, **React** for the frontend, and **SQLite** for lightweight data persistence.

---

## Live API & Frontend (Local)

- **API**: [http://localhost:5000/api/nav/latest](http://localhost:5000/api/nav/history)  
- **Frontend**: [http://localhost:3000](http://localhost:3000)

---

##  Features

###  Real-Time NAV Calculation

Fetches balances from:

- **Ethereum Wallet**: `0x052e3082ED423F790D4D8A4756DC45A9CAf3D544`
- **Solana Wallet**: `BXKDAAAFYrPhkVRvyLHj2AQEa3PStHsBaWSY7errtEiM`

Converts token balances to USD using **CoinGecko API**  
Calculates:
- **Total AUM** (Assets Under Management)
- **NAV per Share** = AUM ÷ 10,000 shares

---

###  Daily NAV Snapshot Storage

- NAV data stored daily in an **SQLite database**
- Each snapshot is **timestamped** for historical logging and audit purposes

---

###  API Endpoints

- `GET /api/nav/latest` – Latest NAV + AUM snapshot  
- `GET /api/nav/history` – Historical NAVs (most recent first)

---
###  Frontend Viewer (React)

- Table view showing NAV, AUM, and share price over time  
- Built with `React Hooks` and `axios`

---

##  Getting Started

### 1. Backend Setup (Flask + SQLite)

cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Create a .env file:

ETHERSCAN_API_KEY=your_key_here

## Run database migrations:

export FLASK_APP=run.py
flask db init        # Only on first run
flask db migrate -m "Init"
flask db upgrade

## 2. Create NAV Snapshot

python3 test_snapshot.py

## Start the server:

flask run

## 3. Frontend Setup (React)

cd frontend
npm install
npm start


##  Tech Stack
Layer	Technology
Backend	Python, Flask
Database	SQLite + SQLAlchemy
Frontend	React.js
Pricing API	CoinGecko
Wallet APIs	Etherscan, Solana RPC

## Future Enhancements
Schedule hourly NAV tracking and use highest of the day

Add frontend share issuance (buy/sell) form

Track staking rewards or asset yields

Add charts to visualize NAV trends

User login & investor dashboards

## Author
## Built by Herman Gathege as a technical challenge submission for the ICM crypto product team.
