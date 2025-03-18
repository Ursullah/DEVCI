import React from 'react'
import { useState, } from 'react';
import { useNavigate } from 'react-router-dom';

const AdminDashboard = () => {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [hospital, setHospital] = useState("");
    const [errors, setErrors] = useState({});

    const navigate = useNavigate();

    const validate = () => {
        const validationErrors = {};
        if (!name) {
            validationErrors.name = "Doctor's ID is required";
        }
        if (!email) {
            validationErrors.email = "Email is required";
        } else if (!/\S+@\S+\.\S+/.test(email)) {
            validationErrors.email = "Invalid email format";
        }
        if (!hospital) {
            validationErrors.hospital = "Hospital name is required"
        }
        setErrors(validationErrors);
        return Object.keys(validationErrors).length === 0;
    };

    
    const handleChange = (e) => {
        const { name, value } = e.target;
        if (name === "name") setName(value);
        else if (name === "hospital") setHospital(value);
        else if (name === "email") setEmail(value);
    };

    const RegisterDoctor = (e) => {
        e.preventDefault(); // Prevent form submission
        if (!validate()) return; // Stop execution if validation fails
        alert("Doctor successfully registered✅")
    }
  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      
      <form onSubmit={RegisterDoctor}className="w-full max-w-md bg-white p-6 rounded-lg shadow-lg">
        <label className="block font-semibold">Doctor's ID:</label>
        <input
          type="text"
          name="name"
          onChange={handleChange}
          placeholder="Doctor's ID"
          className="w-full p-2 border border-gray-300 rounded mb-4"
        />
        {errors.name && <span className="text-red-500 text-xs italic">{errors.name}</span>}

        <label className="block font-semibold">Hospital:</label>
        <input
          type="text"
          name="hospital"
          onChange={handleChange}
          placeholder="HospitalName"
          className="w-full p-2 border border-gray-300 rounded mb-4"
        />
        {errors.hospital && <span className="text-red-500 text-xs italic">{errors.hospital}</span>}

        <label className="block font-semibold">Email Adress:</label>
        <input
          type="text"
          onChange={handleChange}
          name="email"
          placeholder="example@gmail.com"
          className="w-full p-2 border border-gray-300 rounded mb-4"
        />
        {errors.email && <span className="text-red-500 text-xs italic">{errors.email}</span>}

         <button 
           className="bg-indigo-500 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded"
           type="submit">
            Register Doctor
         </button>
        </form>

        {/* Back to Home Button */}
      <div className="text-center mt-6">
        <button onClick={() => navigate("/")} className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600 transition">Back to Home</button>
      </div>


    </div>
  )
}

export default AdminDashboard
// can view audit logs
// can register doctors