// App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './components/AuthContext';
import PrivateRoute from './components/PrivateRoute';

import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import LogsScreen from './components/LogsScreen';
import ScrapedData from './components/ScrapedData';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected Routes */}
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/logs"
            element={
              <PrivateRoute>
                <LogsScreen />
              </PrivateRoute>
            }
          />
          <Route
            path="/scraped-data"
            element={
              <PrivateRoute>
                <ScrapedData />
              </PrivateRoute>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;