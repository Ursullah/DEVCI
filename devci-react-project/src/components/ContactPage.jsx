import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate

const ContactPage = () => {
  const navigate = useNavigate(); // Initialize navigate function
  const [message, setMessage] = useState(""); // State for textarea

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-6 text-gray-800">
      <h2 className="text-3xl font-bold mb-6">Contact Us</h2>

      <form className="w-full max-w-md bg-white p-6 rounded-lg shadow-lg">
        <label className="block font-semibold">Your Name:</label>
        <input
          type="text"
          name="name"
          placeholder="Name"
          className="w-full p-2 border border-gray-300 rounded mb-4"
        />

        <label className="block font-semibold">Email Address:</label>
        <input
          type="text"
          name="email"
          placeholder="example@email.com"
          className="w-full p-2 border border-gray-300 rounded mb-4"
        />

        <label className="block font-semibold">Phone Number:</label>
        <input
          type="text"
          name="number"
          placeholder="0700000000"
          className="w-full p-2 border border-gray-300 rounded mb-4"
        />

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
