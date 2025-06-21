#  ICM NAV Tracker – End-to-End Test Plan

This document outlines step-by-step tests to validate the entire NAV Tracker application — backend, frontend, and logic.

---

##  BACKEND SYSTEM LOGIC

### 1. ETH & SOL Balance + USD Conversion

* **Files:** `app/services/eth.py`, `app/services/solana.py`
* **Command:** `python3 test_nav.py`
* **Expected Output:**

  ```json
  {
    "eth_usd": 810.25,
    "sol_usd": 1325.45,
    "total_aum": 2135.70,
    "nav_per_share": 0.213570
  }
  ```
* **Validates:** Wallet API connection + CoinGecko pricing

---

### 2. Daily Snapshot Creation

* **File:** `app/tasks/daily_nav.py`
* **Command:** `python3 test_snapshot.py`
* **Expected Output:**

  ```bash
   Daily NAV snapshot saved: {...}
  ```
* **Validates:** Snapshot saved to `NavSnapshot`; watermark updates if higher

---

### 3. Config Initialization

* **File:** `scripts/init_config.py`
* **Command:** `PYTHONPATH=. python3 scripts/init_config.py`
* **Expected Output:**

  ```bash
   Default config values inserted.
  ```
* **Validates:** `Config` table includes `total_shares`, `high_nav_watermark`

---

##  API FUNCTIONALITY TESTING

### 4. Get Latest NAV

* **Route:** `GET /api/nav/latest`
* **Tool:** Browser or Postman
* **Expected Output:** JSON snapshot with NAV info

### 5. Buy Shares

* **Route:** `POST /api/buy`
* **Payload:**

  ```json
  { "amount_usd": 500 }
  ```
* **Expected Output:**

  ```json
  {
    "shares_issued": 2341.658,
    "fee_applied": 5.00,
    "nav_used": 0.213570,
    "new_total_shares": 12341.658
  }
  ```
* **Validates:** Purchase logic, flat fee, DB insert

### 6. Sell Shares

* **Route:** `POST /api/sell`
* **Payload:**

  ```json
  { "shares": 500 }
  ```
* **Expected Output:**

  ```json
  {
    "shares_sold": 500.0,
    "amount_returned_usd": 105.32,
    "flat_fee": 1.06,
    "performance_fee": 3.47,
    "nav_used": 0.213570,
    "remaining_total_shares": 11841.658
  }
  ```
* **Validates:** Sell logic, flat + performance fee, DB update

---

##  DATABASE STATE CHECKS

In Python shell or admin panel:

```python
Config.query.filter_by(key="total_shares").first().value
Config.query.filter_by(key="high_nav_watermark").first().value
```

* **Validates:** Internal config state matches app logic

---

##  FRONTEND TESTING

### 7. NAV History Table

* **File:** `components/NavHistory.js`
* **Action:** Load app on `http://localhost:3000`
* **Expect:** Table showing:

  * Timestamp
  * ETH/SOL values
  * AUM
  * NAV/share

### 8. Buy/Sell Form

* **File:** `components/BuySellForm.js`
* **Action:** Use form to buy and sell
* **Expect:**

  * JSON result shown
  * Correct fees, NAV used, shares issued/sold

---

##  BONUS VALIDATION

### Performance Fee Logic

1. Lower watermark in DB manually
2. Take a new NAV snapshot with a higher NAV
3. Sell shares — performance fee should apply only on the profit portion

---

##  FINAL CHECKLIST

| Feature                       | Test Method        | Status |
| ----------------------------- | ------------------ | ------ |
| ETH/SOL balance fetch         | `test_nav.py`      | ✅      |
| NAV snapshot save             | `test_snapshot.py` | ✅      |
| Config variables              | `init_config.py`   | ✅      |
| Latest NAV API                | `/api/nav/latest`  | ✅      |
| Buy shares                    | `/api/buy`         | ✅      |
| Sell shares (fees, watermark) | `/api/sell`        | ✅      |
| Frontend NAV display          | `NavHistory.js`    | ✅      |
| Buy/Sell UI                   | `BuySellForm.js`   | ✅      |

---



