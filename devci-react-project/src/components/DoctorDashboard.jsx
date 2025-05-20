import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import LOGOUT from "./LOGOUT";

const DoctorDashboard = () => {
  const [patientName, setPatientName] = useState("");
  const [patientAge, setPatientAge] = useState("");
  const [info, setInfo] = useState("");
  const [medication, setMedication] = useState("");
  const [medicineId, setMedicineId] = useState('')
  const [dosage, setDosage] = useState("");
  const [message, setMessage] = useState("");
  const [errors, setErrors] = useState({});
  const [prescriptions, setPrescriptions] = useState([]);
  const [searchTerm, setSeaarchTerm] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [showResults, setShowResults] = useState(false);
  const role = localStorage.getItem("role");
  const name = localStorage.getItem("name");
  const doctorId = localStorage.getItem("id");

  // Fetch prescriptions from backend using Axios
  useEffect(() => {
    const fetchPrescriptions = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/api/doctorprescription?id=${doctorId}`);
        setPrescriptions(response.data);
      } catch (err) {
        console.error("Error fetching prescriptions:", err);
      }
    };

    fetchPrescriptions();
  }, []);

  console.log(prescriptions)
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setShowResults(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const searchMedicine = async () => {
    if (!searchTerm.trim()) {
      searchResults([]);
      return;
    }

    try {
      const response = await axios.get(
        `http://localhost:5000/api/searchmedicine?name=${searchTerm}`
      );
      setSearchResults(response.data);
      console.log(response.data);
      setShowResults(true);
    } catch (err) {
      console.error("Error searching medicine", err);
      setSearchResults([]);
    }
  };

  useEffect(() => {
    const debounceTimer = setTimeout(() => {
      if (searchTerm.length > 2) {
        searchMedicine(searchTerm);
      } else {
        searchResults([]);
      }
    }, 300);

    return () => clearTimeout(debounceTimer);
  }, [searchTerm]);

  const selectMedicine = (medicine) => {
    setMedicineId(medicine.id)
    setMedication(medicine.name);
    setSeaarchTerm(medicine.name);
    setShowResults(false);
  };


  const validate = () => {
    const validationErrors = {};
    if (!patientName) validationErrors.patientName = "Patient name is required";
    if (!patientAge) validationErrors.patientAge = "Age is required";
    if (!info) validationErrors.info = "Contact is required";
    if (!medication) validationErrors.medication = "Medicine is required";
    if (!dosage) validationErrors.dosage = "Please select a dosage";

    setErrors(validationErrors);
    return Object.keys(validationErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === "patientName") setPatientName(value);
    else if (name === "patientAge") setPatientAge(value);
    else if (name === "info") setInfo(value);
    else if (name === "dosage") setDosage(value);
    else if (name === "medication") {
      setMedication(value);
      setSeaarchTerm(value);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    const newPrescription = {
      doctorName: name,
      doctorId: doctorId,
      patientName,
      patientAge,
      contact: info,
      medicineId: medicineId,
      medication,
      dosage,
      instructions: message,
    };

    console.log(newPrescription);

    try {
      const response = await axios.post(
        "http://localhost:5000/api/prescriptions",
        newPrescription
      );
      setPrescriptions([...prescriptions, response.data]);

      alert("Patient prescription is saved ✅");

      // Clear input fields
      setPatientName("");
      setPatientAge("");
      setInfo("");
      setMedication("");
      setDosage("");
      setMessage("");
    } catch (error) {
      console.error("Error saving prescription:", error);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-400 flex-col">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded-lg shadow-md w-full max-w-md"
      >
        <h2 className="text-2xl font-bold text-center mb-6">
          Doctor's Prescription
        </h2>

        <div className="mb-4">
          <label className="block font-semibold">Patient's Name:</label>
          <input
            type="text"
            name="patientName"
            value={patientName}
            onChange={handleChange}
            placeholder="Enter patient's name"
            className="w-full p-2 border border-gray-300 rounded mt-1"
          />
          {errors.patientName && (
            <span className="text-red-500 text-sm">{errors.patientName}</span>
          )}
        </div>

        <div className="mb-4">
          <label className="block font-semibold">Patient's Age:</label>
          <input
            type="text"
            name="patientAge"
            value={patientAge}
            onChange={handleChange}
            placeholder="Enter age"
            className="w-full p-2 border border-gray-300 rounded mt-1"
          />
          {errors.patientAge && (
            <span className="text-red-500 text-sm">{errors.patientAge}</span>
          )}
        </div>

        <div className="mb-4">
          <label className="block font-semibold">Contact:</label>
          <input
            type="text"
            name="info"
            value={info}
            onChange={handleChange}
            placeholder="Enter contact number"
            className="w-full p-2 border border-gray-300 rounded mt-1"
          />
          {errors.info && (
            <span className="text-red-500 text-sm">{errors.info}</span>
          )}
        </div>

        <div className="mb-4 relative">
          <label className="block font-semibold">Medicine Name:</label>
          <input
            type="text"
            name="medication"
            value={medication}
            onChange={handleChange}
            onFocus={() => searchTerm && setShowResults(true)}
            onBlur={() => setTimeout(() => setShowResults(false), 200)}
            placeholder="Search medicine..."
            autoComplete="off"
            className="w-full p-2 border border-gray-300 rounded mt-1"
          />
          {errors.medication && (
            <span className="text-red-500 text-sm">{errors.medication}</span>
          )}

          {/* Search results dropdown */}
          {showResults && searchResults.length > 0 && (
            <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded shadow-lg max-h-60 overflow-y-auto">
              {searchResults.map((medicine) => (
                <div
                  key={medicine.id || medicine.name}
                  className="p-2 hover:bg-blue-50 cursor-pointer border-b border-gray-100"
                  onMouseDown={() => selectMedicine(medicine)} // Use onMouseDown to prevent blur
                >
                  <div className="font-medium flex justify-between">
                    <span>{medicine.name}</span>
                    <span className="text-blue-600">KSH {medicine.price}</span>
                  </div>
                  <div className="text-sm text-gray-600">
                    {medicine.stock > 0 ? (
                      <span className="text-green-600">
                        In stock: {medicine.stock}
                      </span>
                    ) : (
                      <span className="text-red-600">Out of stock</span>
                    )}
                  </div>
                  {medicine.expiry_date && (
                    <div className="text-xs text-gray-500">
                      Expires:{" "}
                      {new Date(medicine.expiry_date).toLocaleDateString()}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="mb-4">
          <label className="block font-semibold">Select Dosage:</label>
          <select
            name="dosage"
            value={dosage}
            onChange={handleChange}
            className="w-full p-2 border border-gray-300 rounded mt-1"
          >
            <option value="">Select dosage</option>
            <option value="1×2">1×2</option>
            <option value="2×2">2×2</option>
            <option value="2×3">2×3</option>
            <option value="2×4">2×4</option>
            <option value="3×3">3×3</option>
            <option value="3×1">3×1</option>
          </select>
          {errors.dosage && (
            <span className="text-red-500 text-sm">{errors.dosage}</span>
          )}
        </div>

        <textarea
          name="message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Instructions for medication"
          className="w-full p-2 border border-gray-300 rounded mb-4"
        ></textarea>

        <button
          type="submit"
          className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
        >
          Set Prescription
        </button>
      </form>

      {/* Patient Logs - View Saved Prescriptions */}
      <div className="w-full max-w-2xl mt-8 bg-white p-6 rounded-lg shadow-lg overflow-y-scroll h-[100vh]">
        <h2 className="text-lg font-bold mb-4">Patient Logs</h2>
        {prescriptions.length === 0 ? (
          <p className="text-gray-500">No prescriptions recorded yet.</p>
        ) : (
          <ul>
            {prescriptions.map((prescription, index) => (
              <li key={index} className="border-b py-2">
                <p>
                  <strong>Doctor:</strong> {prescription.doctor_name}
                </p>
                <p>
                  <strong>Patient:</strong> {prescription.patient_name}
                </p>
                <p>
                  <strong>Age:</strong> {prescription.patient_age}
                </p>
                <p>
                  <strong>Contact:</strong> {prescription.contact}
                </p>
                <p>
                  <strong>Medication:</strong> {prescription.medication}
                </p>
                <p>
                  <strong>Dosage:</strong> {prescription.dosage}
                </p>
                <p>
                  <strong>Instructions:</strong>{" "}
                  {prescription.instruction || "N/A"}
                </p>
              </li>
            ))}
          </ul>
        )}
      </div>

      <LOGOUT />
    </div>
  );
};

export default DoctorDashboard;
