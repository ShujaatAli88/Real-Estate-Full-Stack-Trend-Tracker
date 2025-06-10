// components/AuthContext.jsx
import { createContext, useState, useEffect ,useContext} from 'react';
import { Navigate } from 'react-router-dom';

// Simulate authentication check (you can replace this with real auth)
const getAuthStatus = () => {
  return localStorage.getItem('isLoggedIn') === 'true';
};

export const AuthContext = createContext();

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(getAuthStatus());

  useEffect(() => {
    // Optional: listen for auth changes if needed
  }, []);

  const login = () => {
    localStorage.setItem('isLoggedIn', 'true');
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.setItem('isLoggedIn', 'false');
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};