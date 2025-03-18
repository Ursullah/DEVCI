import React from 'react'
import { useNavigate } from "react-router-dom";

const LOGOUT = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("userRole");
    localStorage.removeItem("isAuthenticated");
    navigate("/login"); // Redirect to login page
  };

  return (
    <button
      onClick={handleLogout}
      className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition duration-300 mt-"
    >
      Logout
    </button>
  );
};

export default LOGOUT
