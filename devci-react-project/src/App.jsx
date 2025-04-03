import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useEffect, useState } from "react";
import Layout from "./components/Layout"; // Import Layout
import LogIn from "./components/LogIn";
import RegisterUser from "./components/RegisterUser";
import HomePage from "./components/HomePage";
import AboutPage from "./components/AboutPage";
import ContactPage from "./components/ContactPage";
import PharmacistDashboard from "./components/PharmacistDashboard";
import AdminDashboard from "./components/AdminDashboard";
import DoctorDashboard from "./components/DoctorDashboard";
import Footer from "./components/Footer";


function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return localStorage.getItem("auth") === "true";
  });

  const [userRole, setUserRole] = useState(() =>{
    return localStorage.getItem("auth") === "true";
  });

  useEffect(() => {
    const authStatus = localStorage.getItem("auth") === "true";
    const role = localStorage.getItem("role") || "";
    setIsAuthenticated(authStatus);
    setUserRole(role);
  }, []);

  const handleAuth = (value) => {
    localStorage.setItem("auth", value ? "true" : "false");
    setIsAuthenticated(value);
    setUserRole(value ? localStorage.getItem("role") : "")
  };

  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <div className="flex-grow">
      <Routes>
       
        {/* Protected Routes inside Layout */}
        <Route
          path="/"
          element={isAuthenticated ? <Layout /> : <Navigate to="/login" replace />}>
             <Route path="/login" element={<LogIn setIsAuthenticated={handleAuth} />} />
          <Route index element={<HomePage setIsAuthenticated={handleAuth} />} />
          <Route path="about" element={<AboutPage />} />
          <Route path="contact" element={<ContactPage />} />
          <Route path="register" element={<RegisterUser/>} />
          <Route path="doctordashboard" element={<DoctorDashboard />} />
          <Route path="admindashboard" element={<AdminDashboard />} />
          <Route path="pharmacistdashboard" element={<PharmacistDashboard />} />

          {isAuthenticated ? (
            <>
            <Route path="pharmacist-dashboard" element={<PharmacistDashboard />} />
            <Route path="/doctor-dashboard" element={<DoctorDashboard />} />
            <Route path="/admin-dashboard" element={<AdminDashboard />} />
            </>
           ) : (
            <Route path="*" element={<Navigate to="/login" replace />} />
           )}
        </Route>
      </Routes>
      </div>
      <Footer />
      </div>
    </Router>
  );
}

export default App;
