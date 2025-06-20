import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/NavHistory.css'; // Import the custom CSS

const NavHistory = () => {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/api/nav/history')
      .then(res => setHistory(res.data))
      .catch(err => console.error("Error fetching NAV history:", err));
  }, []);

  return (
    <div className="nav-history-container">
      <h2 className="nav-history-title">📈 NAV / AUM History</h2>
      <div className="table-wrapper">
        <table className="nav-history-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>ETH (USD)</th>
              <th>SOL (USD)</th>
              <th>Total AUM</th>
              <th>NAV / Share</th>
            </tr>
          </thead>
          <tbody>
            {history.length === 0 ? (
              <tr>
                <td colSpan="5" className="empty-row">No data available</td>
              </tr>
            ) : (
              history.map(entry => (
                <tr key={entry.id}>
                  <td>{new Date(entry.timestamp).toLocaleString()}</td>
                  <td>${entry.eth_usd.toFixed(2)}</td>
                  <td>${entry.sol_usd.toFixed(2)}</td>
                  <td>${entry.total_aum.toFixed(2)}</td>
                  <td>${entry.nav_per_share.toFixed(6)}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default NavHistory;
