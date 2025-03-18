import React from "react";
import { useNavigate } from "react-router-dom"; // Import navigation hook

const AboutPage = () => {
  const navigate = useNavigate(); 

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-900 p-6 text-white">
      <header className=" bg-red-700 py-6 text-center shadow-md rounded-4xl">
        <h1 className="text-4xl font-bold mb-4">ABOUT US</h1>
      </header>

      <main className="flex flex-col items-center justify-center flex-1 p-8">
      <img
        src="/assets/consulting.jpg" 
        alt="About Us"
        className="w-full max-w-lg h-64 object-cover rounded-lg shadow-lg mx-auto mb-6"
      /> 

       <p className="text-lg text-center max-w-3xl mb-4">
        <strong className="text-red-400">Who we are:</strong> Prescription Verifier is a cutting-edge web-based
        platform that enhances prescription authentication in pharmacies and healthcare facilities.
      </p>

      <p className="text-lg leading-relaxed mb-6">
        <strong className="text-red-400">Our Mission:</strong> <br />
        To eliminate prescription fraud by providing a reliable, efficient, and user-friendly verification system.
      </p>

         <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-bold text-red-400 mb-4">Why Choose Us?</h2>
            <ul className="text-lg space-y-3">
              <li><strong className="text-red-300">🔹 Patient Safety:</strong> Reduces the risk of dispensing medication based on fraudulent prescriptions.</li>
              <li><strong className="text-red-300">🔹 Efficiency:</strong> Saves time and minimizes errors in pharmacies.</li>
              <li><strong className="text-red-300">🔹 Legal Compliance:</strong> Helps pharmacies adhere to healthcare regulations.</li>
            </ul>
          </div>    
        </main>
      

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
