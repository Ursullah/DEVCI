import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useEffect, useState } from "react";
import Header from "./components/Header";
import LogIn from './components/LogIn';
import HomePage from "./components/HomePage";
import PharmacistDashboard from "./components/PharmacistDashboard";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return localStorage.getItem("auth") === "true";
  });

  useEffect(() => {
    const authStatus = localStorage.getItem("auth") === "true";
    setIsAuthenticated(authStatus);
  }, []);

  const handleAuth = (value) => {
    localStorage.setItem("auth", value ? "true" : "false");
    setIsAuthenticated(value);
  };

  return (
    <Router>
      <Routes>
        {/* Login Route */}
        <Route path="/login" element={<LogIn setIsAuthenticated={handleAuth} />} />
        
        {/* Home Route (Protected) */}
        <Route
          path="/home"
          element={isAuthenticated ? (
            <>
              <Header setIsAuthenticated={handleAuth} />
              <HomePage setIsAuthenticated={handleAuth} />
            </>
          ) : (
            <Navigate to="/login" replace />
          )}
        />
        <Route path="/pharmacist" element={<PharmacistDashboard />} />
        {/* Default Route */}
        <Route path="*" element={<Navigate to={isAuthenticated ? "/home" : "/login"} />} />
      </Routes>
    </Router>
  );
}

export default App;
