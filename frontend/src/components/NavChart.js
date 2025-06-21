import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  ReferenceLine,
} from "recharts";

const NavChart = () => {
  const [data, setData] = useState([]);
  const [watermark, setWatermark] = useState(null);

  useEffect(() => {
    // Fetch NAV history
    axios.get("http://localhost:5000/api/nav/history").then((res) => {
      const formatted = res.data.map((entry) => ({
        ...entry,
        date: new Date(entry.timestamp).toLocaleDateString("en-GB", {
          day: "2-digit",
          month: "short",
        }),
      }));
      setData(formatted.reverse()); // oldest first
    });

    // Fetch watermark value from backend
    axios.get("http://localhost:5000/api/config").then((res) => {
      const wm = res.data.find((item) => item.key === "high_nav_watermark");
      setWatermark(wm?.value || null);
    });
  }, []);

  // Get latest snapshot safely
  const latest = data[data.length - 1];

  return (
    <div style={{ padding: "2rem" }}>
      {/* 📊 NAV Stat Card */}
      {latest && (
        <div
          style={{
            backgroundColor: "#f9f9f9",
            padding: "1.5rem",
            borderRadius: "1rem",
            textAlign: "center",
            boxShadow: "0 2px 6px rgba(0,0,0,0.05)",
            marginBottom: "2rem",
          }}
        >
          <h3 style={{ color: "#444" }}>Current NAV Per Share</h3>
          <h1
            style={{
              color: "#4a90e2",
              fontSize: "3rem",
              margin: "0.5rem 0",
            }}
          >
            ${latest.nav_per_share.toFixed(4)}
          </h1>
          <p style={{ color: "#888" }}>As of {latest.date}</p>
        </div>
      )}

      {/* 📈 NAV & AUM Line Chart */}
      <h2>NAV & AUM Performance</h2>
      <ResponsiveContainer width="100%" height={350}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis
            yAxisId="left"
            label={{ value: "Value (USD)", angle: -90, position: "insideLeft" }}
          />
          <Tooltip />
          <Legend />

          <Line
            yAxisId="left"
            type="monotone"
            dataKey="nav_per_share"
            stroke="#8884d8"
            strokeWidth={2}
            name="NAV per Share"
          />
          <Line
            yAxisId="left"
            type="monotone"
            dataKey="total_aum"
            stroke="#00bcd4"
            strokeWidth={2}
            name="Total AUM"
          />

          {watermark && (
            <ReferenceLine
              yAxisId="left"
              y={watermark}
              stroke="red"
              strokeDasharray="3 3"
              label={{
                value: `Watermark: $${watermark.toFixed(4)}`,
                position: "top",
                fill: "red",
                fontSize: 12,
              }}
            />
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default NavChart;
