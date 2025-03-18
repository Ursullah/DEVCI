import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

const HomePage = ({ setIsAuthenticated }) => {
  const [selectedRole, setSelectedRole] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const role = localStorage.getItem("role") || "Guest";
    console.log("User Role:", role);
    setSelectedRole(role);
  }, [setSelectedRole]);

  const handleLogin = () =>{
    setIsAuthenticated(false);
    navigate("/login");
  };

  return (
    <div className="relative w-full min-h-screen bg-slate-900 flex items-center justify-center px-8">
      <div className="max-w-5xl w-full flex flex-col md:flex-row items-center text-white">
        
        {/* Text Section */}
        <motion.div 
          initial={{ opacity: 0, x: -50 }} 
          animate={{ opacity: 1, x: 0 }} 
          transition={{ duration: 1 }}
          className="md:w-1/2 text-center md:text-left"
        >
          <h2 className="text-3xl font-bold">Here to provide your medicine solution!</h2>
          <p className="text-lg mt-4 leading-relaxed">
            Our Prescription Verifier System is designed to ensure the accuracy and authenticity of medical prescriptions, 
            helping healthcare providers and pharmacists prevent errors and unauthorized prescriptions. 
            By securely validating prescriptions against a trusted database, the system reduces the risk of fraud and enhances patient safety.
            With an intuitive interface and real-time verification, it streamlines the prescription process, making medication dispensing more secure and efficient.
          </p>
          <button
            type="button" onClick={() => navigate("/login")}
            className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition duration-300 cursor-pointer mt-4"
          >
          LOGIN
          </button>
        </motion.div>

        {/* Image Section with Animation */}
        <motion.img 
          src="/assets/consulting.jpg" 
          alt="Consulting"
          initial={{ opacity: 0, x: 50 }} 
          animate={{ opacity: 1, x: 0 }} 
          transition={{ duration: 1.2 }}
          className="md:w-1/2 rounded-3xl shadow-lg"
        />
      </div>
    </div>
  );
};

export default HomePage;
