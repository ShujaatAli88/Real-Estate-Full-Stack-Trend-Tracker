import React, { useEffect, useState, useContext } from 'react';
import './Dashboard.css';
import { FaHome, FaChartLine, FaUserCircle, FaDatabase, FaSpider, FaAppStore, FaSignOutAlt, FaUserAstronaut, FaUserGraduate, FaPersonBooth, FaVoicemail, FaMailBulk, FaGem } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from './AuthContext'; // Adjust path if needed
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Area, Legend
} from 'recharts';

const Dashboard = () => {
  const [avgPrice, setAvgPrice] = useState(null);
  const [totalListings, setTotalListings] = useState(null);
  const [priceTrends, setPriceTrends] = useState([]);
  const [showProfilePopup, setShowProfilePopup] = useState(false);
  const [userData, setUserData] = useState(null);

  const navigate = useNavigate();
  const { logout } = useContext(AuthContext);

  const handleScrapedData = () => {
    navigate('/scraped-data');
  };

  const handleRunCrawler = () => {
    navigate('/logs');
  };

  const handleLogout = () => {
    logout(); // Update auth state
    navigate('/'); // Redirect to login
  };

  useEffect(() => {
    // Simulated user data — replace with real API call if needed
    const mockUserData = {
      name: "Shujaat Ali",
      email: "shujaatalee888@gmail.com",
      age: 30
    };
    setUserData(mockUserData);
  }, []);

  useEffect(() => {
    fetch('http://localhost:5000/api/price-trends')
      .then(res => res.json())
      .then(data => setPriceTrends(data))
      .catch(err => console.error('Error fetching price trends:', err));
  }, []);

  useEffect(() => {
    fetch('http://localhost:5000/api/average-price')
      .then(res => res.json())
      .then(data => {
        setAvgPrice(data.averagePrice);
      })
      .catch(err => console.error('Error fetching average price:', err));

    fetch('http://localhost:5000/api/total-listings')
      .then(res => res.json())
      .then(data => {
        setTotalListings(data.totalListings);
      })
      .catch(err => console.error('Error fetching total listings:', err));
  }, []);

  return (
    <div className="dashboard">
      {/* Navbar */}
      <nav className="navbar">
        <div className="navbar-left">
          <span className="logo"><FaAppStore /> Zillow.com Tracker PRO</span>
          <ul className="nav-links">
            <li onClick={handleScrapedData}><FaDatabase /> Scraped Data</li>
            <button className="run-crawler-btn" onClick={handleRunCrawler}>
              <li><FaSpider /> Run Crawler</li>
            </button>
          </ul>
        </div>
        <div className="navbar-right">
          <ul className="nav-links">
            <li onClick={() => setShowProfilePopup(true)}><FaUserCircle /> Profile</li>
          </ul>
        </div>
      </nav>

      {/* Main Content */}
      <main className="main-content">
        <header className="dashboard-header">
          <h1>📊 Quick Insights</h1>
          <p>Insights into your real estate activity and trends</p>
        </header>

        {/* Stats Cards */}
        <section className="cards">
          <div className="card highlight-card">
            <h3>🏠 Total Listings</h3>
            <p>{totalListings !== null ? totalListings.toLocaleString() : 'Loading...'}</p>
          </div>
          <div className="card highlight-card">
            <h3>🆕 New Listings This Week</h3>
            <p>87</p>
          </div>
          <div className="card highlight-card">
            <h3>💲 Avg. Price</h3>
            <p>{avgPrice !== null ? `$${avgPrice.toLocaleString()}` : 'Loading...'}</p>
          </div>
        </section>

        {/* Chart Section */}
        <section className="chart-section">
          <h2 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <FaChartLine color="#8884d8" /> Price Trends Over Time
          </h2>

          {priceTrends.length > 0 && (
            <div className="trend-summary">
              <strong>Latest Avg. Price:</strong>{' '}
              ${priceTrends[priceTrends.length - 1].average.toLocaleString()}
            </div>
          )}

          <div className="chart-container" style={{ height: '300px' }}>
            {priceTrends.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={priceTrends} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorAverage" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
                      <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#fff', border: '1px solid #ccc' }}
                    labelStyle={{ color: '#8884d8' }}
                    formatter={(value) => [`$${value.toLocaleString()}`, 'Avg. Price']}
                  />
                  <Legend verticalAlign="top" height={36} />
                  <Line
                    type="monotone"
                    dataKey="average"
                    stroke="#8884d8"
                    strokeWidth={3}
                    dot={{ stroke: '#8884d8', strokeWidth: 2, r: 4 }}
                    activeDot={{ r: 6 }}
                    isAnimationActive={true}
                    animationDuration={800}
                  />
                  <Area type="monotone" dataKey="average" fillOpacity={0.3} fill="url(#colorAverage)" />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <p>Loading chart...</p>
            )}
          </div>
        </section>
      </main>

      {/* Profile Popup Modal */}
      {showProfilePopup && (
        <div className="profile-modal-overlay">
          <div className="profile-modal">
            <button className="profile-modal-close" onClick={() => setShowProfilePopup(false)}>×</button>
            <h3><FaUserGraduate/> My Info</h3>
            {userData ? (
              <>
                <p><strong><FaUserCircle/> :</strong> {userData.name}</p>
                <p><strong><FaMailBulk/> :</strong> {userData.email}</p>
                <p><strong><FaGem/> Age:</strong> {userData.age}</p>
                <button className="profile-logout-btn" onClick={handleLogout}>
                  <FaSignOutAlt /> Logout
                </button>
              </>
            ) : (
              <p>Loading user info...</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;