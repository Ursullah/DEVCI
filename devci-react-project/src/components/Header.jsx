import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";

const Header = ({ setIsAuthenticated }) => {
  const navigate = useNavigate();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [selectedRole, setSelectedRole] = useState("Select Role");

  const roles = ["Doctor", "Pharmacist", "Admin"];

  const handleLogout = () => {
    setIsAuthenticated(false);
    localStorage.removeItem("auth"); //clear stored role
    localStorage.removeItem("role");
    navigate("/login"); // Redirect to login page
  };

  const handleRoleSelect = (role) => {
    setSelectedRole(role);
    localStorage.setItem("role", role); //store role in local storage
    setIsDropdownOpen(false);
    if (role === "Pharmacist"){
      navigate("/pharmacist")
    } else if (role === "Doctor"){
    navigate("/doctor-dashboard")
    }else{
      navigate("/home")
    }
  };

  return (
    
    <header className="relative bg-gray-900 text-white py-4 px-6 flex justify-between items-center shadow-md z-50">
      <h2 className="text-2xl font-bold">DEVCI</h2>

      {/* Centered Navigation */}
      <nav className="absolute left-1/2 transform -translate-x-1/2 flex space-x-6">
        <Link to="/home" className="hover:text-blue-400 transition duration-200">Home</Link>
        <Link to="/about" className="hover:text-blue-400 transition duration-200">About Us</Link>
        <Link to="/contact" className="hover:text-blue-400 transition duration-200">Contact</Link>
        
        {/* Dropdown Menu */}
        <div className="relative">
          <button 
            onClick={() => setIsDropdownOpen(!isDropdownOpen)} 
            className="bg-gray-700 px-4 py-2 rounded-md hover:bg-gray-600 transition"
          >
            {selectedRole}
          </button>
          
          {isDropdownOpen && (
            <div className="absolute right-0 mt-2 w-40 bg-white text-black rounded-lg shadow-lg z-50">
              <ul className="py-2">
                {roles.map((role) => (
                  <li key={role}>
                    <button 
                      onClick={() => handleRoleSelect(role)}
                      className="block px-4 py-2 hover:bg-gray-200 w-full text-left"
                    >
                      {role}
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </nav>

      {/* Right Side: Logout Button */}
      <button 
        onClick={handleLogout} 
        className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition duration-300 cursor-pointer"
      >
        Logout
      </button>
    </header>
  );
};

export default Header;
