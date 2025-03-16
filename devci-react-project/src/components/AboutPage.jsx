import React from "react";
import { useNavigate } from "react-router-dom"; // Import navigation hook

const AboutPage = () => {
  const navigate = useNavigate(); // Initialize navigate function

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-800 p-6 text-white">
      <h1 className="text-4xl font-bold mb-4">About Us</h1>

      {/* Image Placeholder */}
      <img
        src="/assets/consulting.jpg" 
        alt="About Us"
        className="w-96 h-56 object-cover rounded-lg shadow-lg mb-6"
      />

      <p className="text-lg text-center max-w-3xl mb-4">
        <strong>Who we are:</strong> Prescription Verifier is a cutting-edge web-based
        platform that enhances prescription authentication in pharmacies and healthcare facilities.
      </p>

      <p className="text-lg text-center max-w-3xl mb-4">
        <strong>Our Mission:</strong> <br />
        To eliminate prescription fraud by providing a reliable, efficient, and user-friendly verification system.
      </p>

      <p className="text-lg text-center max-w-3xl mb-4">
        <strong>Why Choose Us?</strong> <br />
        <strong>Patient Safety:</strong> Reduces the risk of dispensing medication based on fraudulent prescriptions. <br />
        <strong>Efficiency:</strong> Saves time and minimizes errors in pharmacies. <br />
        <strong>Legal Compliance:</strong> Helps pharmacies adhere to healthcare regulations.
      </p>

      {/* Back Button */}
      <button 
        onClick={() => navigate("/")} 
        className="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-lg transition duration-300 mt-4"
      >
        ← Back to Home
      </button>
    </div>
  );
};

export default AboutPage;
