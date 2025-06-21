import React from "react";
import NavHistory from "./components/NavHistory";
import BuySellForm from "./components/BuySellForm";
import NavChart from './components/NavChart';

import "./App.css"; // Make sure path matches

function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>ICM NAV Tracker</h1>
      </header>

      <main className="app-main">
        <section className="section">
          <h2 style={{ textAlign: "center" }}>Welcome to the ICM NAV Tracker</h2>
          <p style={{ textAlign: "center" }}>
            This application allows you to track the Net Asset Value (NAV) of
            the ICM fund, view historical data, and buy or sell shares.
          </p>
          <p style={{ textAlign: "center" }}>
            Use the navigation below to explore the features.
          </p>
        </section>

        <section className="section">
          <NavChart />
        </section>

        <section className="section">
          <BuySellForm />
        </section>

        <section className="section">
          <NavHistory />
        </section>
      </main>

      <footer className="app-footer">
        <p>© 2025 ICM. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
