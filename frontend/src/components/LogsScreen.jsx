import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LogsScreen.css';

const LogsScreen = () => {
  const [logs, setLogs] = useState([]);
  const navigate = useNavigate();
  const [eventSource, setEventSource] = useState(null);

  useEffect(() => {
    const source = new EventSource('http://localhost:5000/api/run-crawler');
    setEventSource(source);

    source.onmessage = (e) => {
      setLogs((prevLogs) => [...prevLogs, e.data]);
    };

    source.onerror = (err) => {
      console.error('SSE error:', err);
      source.close();
    };

    return () => {
      source.close(); // Cleanup
    };
  }, []);

  useEffect(() => {
    const box = document.querySelector('.logs-box');
    if (box) {
      box.scrollTop = box.scrollHeight;
    }
  }, [logs]); // <-- runs every time logs change

  const handleStopCrawler = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/stop-crawler', {
        method: 'POST',
      });
      const data = await res.json();
      alert(data.message);
      eventSource && eventSource.close();
    } catch (err) {
      alert('Failed to stop crawler.');
      console.error(err);
    }
  };

  return (
    <div className="logs-screen">
  <div className="logs-container">
    <div className="logs-header">
      <h2>🛠️ Crawler Logs</h2>
      <div className="button-group">
        <button className="back-button" onClick={() => navigate('/dashboard')}>
          ← Back to Dashboard
        </button>
        <button className="stop-button" onClick={handleStopCrawler}>
          ⛔ Stop Crawler
        </button>
      </div>
    </div>

    <div className="logs-box">
      {logs.map((log, index) => (
        <div key={index} className="log-line">
          {log}
        </div>
      ))}
    </div>
  </div>
</div>
  );
};

export default LogsScreen;
