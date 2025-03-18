import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; 

const ContactPage = () => {
  const[name, setName] = useState ("");
  const[email, setEmail] = useState("")
  const[phoneNumber, setPhoneNumber] = useState("")
  const[message, setMessage] = useState("")
  const [errors, setErrors] = useState("")
  const navigate = useNavigate(); 

  
  const validate = () => {
    const validationErrors = {};
    if (!name) {
        validationErrors.name = "Name is required";
    }
    if (!email) {
        validationErrors.email = "Email is required";
    } else if (!/\S+@\S+\.\S+/.test(email)) {
        validationErrors.email = "Invalid email format";
    }
    if (!phoneNumber) {
        validationErrors.phoneNumber = "Phone Number is required";
    }
    if (!message) {
        validationErrors.message = "Enter message";
    }

    setErrors(validationErrors);
    return Object.keys(validationErrors).length === 0;
   };

   const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === "name") setName(value);
    else if (name === "email") setEmail(value);
    else if (name === "phoneNumber") setPhoneNumber(value);
    else if (name === "message") setMessage(value);
};


   const handleSubmit = (e) =>{
    e.preventDefault(); // Prevent form submission
    if (!validate()) return; // Stop execution if validation fails
    alert("Message sent successafully")
   }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-6 text-gray-800">
      <h2 className="text-3xl font-bold mb-6">Contact Us</h2>

      <form onSubmit={handleSubmit}className="w-full max-w-md bg-white p-6 rounded-lg shadow-lg">
        <label className="block font-semibold">Your Name:</label>
        <input
          type="text"
          name="name"
          value={name}
          onChange={handleChange}
          placeholder="Name"
          className="w-full p-2 border border-gray-300 rounded mb-4"
        />
        {errors.name && <span className="text-red-500 text-xs italic">{errors.name}</span>}

        <label className="block font-semibold">Email Address:</label>
        <input
          type="text"
          name="email"
          value={email}
          onChange={handleChange}
          placeholder="example@email.com"
          className="w-full p-2 border border-gray-300 rounded mb-4"
        />
        {errors.email && <span className="text-red-500 text-xs italic">{errors.email}</span>}

        <label className="block font-semibold">Phone Number:</label>
        <input
          type="text"
          name="phoneNumber"
          value={phoneNumber}
          onChange={handleChange}
          placeholder="0700000000"
          className="w-full p-2 border border-gray-300 rounded mb-4"
        />
        {errors.phoneNumber && <span className="text-red-500 text-xs italic">{errors.phoneNumber}</span>}

        <label className="block font-semibold">Your Message:</label>
        <textarea
          name="message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Enter your message"
          className="w-full p-2 border border-gray-300 rounded mb-4"
        ></textarea>

        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition duration-300 w-full"
        >
          Send
        </button>
      </form>

      {/* Back Button */}
      <button
        onClick={() => navigate("/")}
        className="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-lg transition duration-300 mt-6"
      >
        ← Back to Home
      </button>
    </div>
  );
};

export default ContactPage;
