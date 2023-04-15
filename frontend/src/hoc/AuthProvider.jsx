import React from 'react';
import { createContext, useState } from 'react';

export const AuthContext = createContext(null);

export const AuthProvider = ({children}) => {
    const [token, setToken] = useState(null);
  
    const handleLogin = async (newToken, cb) => {
      setToken(newToken);
      cb();
    };
  
    const handleLogout = (cb) => {
      setToken(null);
      cb();
    };
  
    const value = {
      token,
      onLogin: handleLogin,
      onLogout: handleLogout,
    };
  
    return (
      <AuthContext.Provider value={value}>
        {children}
      </AuthContext.Provider>
    );
};