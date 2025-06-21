import React, { useState } from "react";
import axios from "axios";
import "../styles/BuySellForm.css"; // import CSS here

const BuySellForm = () => {
  const [mode, setMode] = useState("buy");
  const [input, setInput] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const url = `http://localhost:5000/api/${mode}`;
    const payload =
      mode === "buy"
        ? { amount_usd: parseFloat(input) }
        : { shares: parseFloat(input) };

    try {
      const res = await axios.post(url, payload);
      setResult(res.data);
    } catch (err) {
      setResult({
        error: err.response?.data?.error || "Something went wrong.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="buy-sell-form">
      <h2>Buy / Sell Shares</h2>
      <div className="mode-buttons">
        <button
          className="buy-btn"
          onClick={() => {
            setMode("buy");
            setResult(null);
          }}
        >
          Buy
        </button>
        <button
          className="sell-btn"
          onClick={() => {
            setMode("sell");
            setResult(null);
          }}
        >
          Sell
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        <label>
          {mode === "buy" ? "Amount (USD)" : "Shares to Sell"}:
          <input
            type="number"
            step="0.01"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            required
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading
            ? "Processing..."
            : mode === "buy"
            ? "Buy Shares"
            : "Sell Shares"}
        </button>
      </form>

      {result && (
        <div className="result">
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default BuySellForm;
