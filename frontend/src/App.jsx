import React, { useEffect, useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

const initialForm = {
  temperature: 60,
  vibration: 30,
  pressure: 120,
  humidity: 45,
  runtime_hours: 300,
};

export default function App() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  async function fetchHistory() {
    const res = await fetch(`${API_BASE}/history`);
    const data = await res.json();
    setHistory(data);
  }

  useEffect(() => {
    fetchHistory();
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    const res = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        temperature: Number(form.temperature),
        vibration: Number(form.vibration),
        pressure: Number(form.pressure),
        humidity: Number(form.humidity),
        runtime_hours: Number(form.runtime_hours),
      }),
    });

    const data = await res.json();
    setResult(data);
    setLoading(false);
    fetchHistory();
  }

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  return (
    <div className="container">
      <h1>AI Predictive Maintenance Dashboard</h1>

      <div className="grid">
        <div className="card">
          <h2>Machine Sensor Input</h2>
          <form onSubmit={handleSubmit}>
            <label>
              Temperature
              <input name="temperature" type="number" value={form.temperature} onChange={handleChange} />
            </label>

            <label>
              Vibration
              <input name="vibration" type="number" value={form.vibration} onChange={handleChange} />
            </label>

            <label>
              Pressure
              <input name="pressure" type="number" value={form.pressure} onChange={handleChange} />
            </label>

            <label>
              Humidity
              <input name="humidity" type="number" value={form.humidity} onChange={handleChange} />
            </label>

            <label>
              Runtime Hours
              <input name="runtime_hours" type="number" value={form.runtime_hours} onChange={handleChange} />
            </label>

            <button type="submit" disabled={loading}>
              {loading ? "Predicting..." : "Predict Failure"}
            </button>
          </form>
        </div>

        <div className="card">
          <h2>Prediction Result</h2>
          {result ? (
            <>
              <p><strong>Status:</strong> {result.status}</p>
              <p><strong>Failure Probability:</strong> {(result.failure_probability * 100).toFixed(2)}%</p>
              <p><strong>Message:</strong> {result.message}</p>
            </>
          ) : (
            <p>No prediction yet.</p>
          )}
        </div>
      </div>

      <div className="card">
        <h2>Recent Predictions</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Temp</th>
              <th>Vibration</th>
              <th>Pressure</th>
              <th>Humidity</th>
              <th>Runtime</th>
              <th>Probability</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {history.map((row) => (
              <tr key={row.id}>
                <td>{row.id}</td>
                <td>{row.temperature}</td>
                <td>{row.vibration}</td>
                <td>{row.pressure}</td>
                <td>{row.humidity}</td>
                <td>{row.runtime_hours}</td>
                <td>{(row.failure_probability * 100).toFixed(1)}%</td>
                <td>{row.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
