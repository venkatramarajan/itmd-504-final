import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setUser({ token, isAdmin: localStorage.getItem('isAdmin') === 'true' });
    }
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    try {
      const response = await axios.post('/api/login', {
        username,
        password,
      });
      const { access_token, is_admin } = response.data;
      localStorage.setItem('token', access_token);
      localStorage.setItem('isAdmin', is_admin);
      setUser({ token: access_token, isAdmin: is_admin });
      return true;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('isAdmin');
    setUser(null);
  };

  const register = async (username, password) => {
    try {
      await axios.post(
        '/api/register',
        { username, password },
        {
          headers: { Authorization: `Bearer ${user.token}` },
        }
      );
      return true;
    } catch (error) {
      console.error('Registration error:', error);
      return false;
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, register, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}; 