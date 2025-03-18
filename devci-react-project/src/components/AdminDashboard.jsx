import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
// import LOGOUT from './LOGOUT';
const AdminDashboard = () => {
    const [doctors, setDoctors] = useState([]);
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [hospital, setHospital] = useState("");
    const [errors, setErrors] = useState({});
    const [editingDoctor, setEditingDoctor] = useState(null); 
    const [specialization, setSpecialization] = useState("")
    const [auditLogs, setAuditLogs] = useState([]);
    const [prescriptions, setPrescriptions] = useState([]);
    const navigate = useNavigate();

      // Fetch data from the backend
  useEffect(() => {
    fetch("http://localhost:5000/doctors")
      .then((res) => res.json())
      .then((data) => setDoctors(data))
      .catch((err) => console.error("Error fetching doctors:", err));

    fetch("http://localhost:5000/audit-logs")
      .then((res) => res.json())
      .then((data) => setAuditLogs(data))
      .catch((err) => console.error("Error fetching audit logs:", err));

    fetch("http://localhost:5000/prescriptions")
      .then((res) => res.json())
      .then((data) => setPrescriptions(data))
      .catch((err) => console.error("Error fetching prescriptions:", err));
  }, []);

    const validate = () => {
        const validationErrors = {};
        if (!name) validationErrors.name = "Doctor's ID is required";
        if (!email) {
            validationErrors.email = "Email is required";
        } else if (!/\S+@\S+\.\S+/.test(email)) {
            validationErrors.email = "Invalid email format";
        }
        if (!hospital) validationErrors.hospital = "Hospital name is required";
        if(!specialization) {
            validationErrors.specialization = "Add doctor's specialization"
        }
        
        setErrors(validationErrors);
        return Object.keys(validationErrors).length === 0;
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        if (name === "name") setName(value);
        else if (name === "hospital") setHospital(value);
        else if (name === "email") setEmail(value);
        else if (name === "specialization") setSpecialization(value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!validate()) return;
         
        const doctorData = { name, email, hospital, specialization };

        if (editingDoctor !== null) {
            // Send PUT request to update doctor
            await fetch(`http://localhost:5000/doctors/${editingDoctor}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(doctorData),
            });
    
            alert("Doctor updated successfully!");
        } else {
            // Send POST request to register a new doctor
            await fetch("http://localhost:5000/doctors", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(doctorData),
            });
    
            alert("Doctor registered successfully!");
        }
        setName("");
        setEmail("");
        setHospital("");
        setSpecialization("");
        alert("Doctor successfully registered ✅");

        fetchDoctor();
    };

    const handleDelete = async (doctorId) => {
        if (!window.confirm("Are you sure you want to delete this doctor?")) return;

        await fetch(`http://localhost:5000/doctors/${doctorId}`, {
            method: "DELETE",
        });
    
        alert("Doctor deleted successfully");
    
        // Refresh doctor list
        fetchDoctors();
    };

    const handleEdit = (index) => {
        const doctor = doctors[index];
        setName(doctor.name);
        setEmail(doctor.email);
        setHospital(doctor.hospital);
        setSpecialization(doctor.specialization);
        setEditingDoctor(index);
    };

    return (
        <div className="flex flex-col items-center min-h-screen bg-gray-100">
            <h1 className="text-2xl font-bold text-center mb-4">ADMIN'S DASHBOARD</h1>
            <form onSubmit={handleSubmit} className="w-full max-w-md bg-white p-6 rounded-lg shadow-lg">
                <h2 className="text-lg font-bold mb-4">{editingDoctor !== null ? "Edit Doctor" : "Register Doctor"}</h2>

                <label className="block font-semibold">Doctor's ID:</label>
                <input
                    type="text"
                    name="name"
                    value={name}
                    onChange={handleChange}
                    placeholder="Doctor's ID"
                    className="w-full p-2 border border-gray-300 rounded mb-4"
                />
                {errors.name && <span className="text-red-500 text-xs italic">{errors.name}</span>}

                <label className="block font-semibold">Hospital:</label>
                <input
                    type="text"
                    name="hospital"
                    value={hospital}
                    onChange={handleChange}
                    placeholder="Hospital Name"
                    className="w-full p-2 border border-gray-300 rounded mb-4"
                />
                {errors.hospital && <span className="text-red-500 text-xs italic">{errors.hospital}</span>}

                <label className="block font-semibold">Email Address:</label>
                <input
                    type="email"
                    name="email"
                    value={email}
                    onChange={handleChange}
                    placeholder="example@gmail.com"
                    className="w-full p-2 border border-gray-300 rounded mb-4"
                />
                {errors.email && <span className="text-red-500 text-xs italic">{errors.email}</span>}

                <label className="block font-semibold">Specialization:</label>
                <input
                    type="name"
                    name="specialization"
                    value={specialization}
                    onChange={handleChange}
                    placeholder="General Practitioner"
                    className="w-full p-2 border border-gray-300 rounded mb-4"
                />
                {errors.specialization && <span className="text-red-500 text-xs italic">{errors.specialization}</span>}

                <button 
                    className="bg-indigo-500 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded w-full"
                    type="submit"
                >
                    {editingDoctor !== null ? "Update Doctor" : "Register Doctor"}
                </button>
            </form>

            {/* Doctors List */}
            <div className="w-full max-w-2xl mt-8 bg-white p-6 rounded-lg shadow-lg">
                <h2 className="text-lg font-bold mb-4">Registered Doctors</h2>
                {doctors.length === 0 ? (
                    <p className="text-gray-500">No doctors registered.</p>
                ) : (
                    <ul>
                        {doctors.map((doctor, index) => (
                            <li key={index} className="flex justify-between items-center border-b py-2">
                                <div>
                                    <p><strong>ID:</strong> {doctor.name}</p>
                                    <p><strong>Hospital:</strong> {doctor.hospital}</p>
                                    <p><strong>Email:</strong> {doctor.email}</p>
                                    <p><strong>Specialization:</strong>{doctor.specialization}</p>
                                </div>
                                <div>
                                    <button 
                                        onClick={() => handleEdit(index)}
                                        className="bg-blue-500 text-white px-3 py-1 rounded mr-2 hover:bg-blue-700"
                                    >
                                        Edit
                                    </button>
                                    <button 
                                        onClick={() => handleDelete(index)}
                                        className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-700"
                                    >
                                        Delete
                                    </button>
                                </div>
                            </li>
                        ))}
                    </ul>
                )}
            </div>

            {/* Back to Home Button */}
            <div className="text-center mt-6">
                <button 
                    onClick={() => navigate("/")} 
                    className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition"
                >
                    Back to Home
                </button>
            </div>
            {/* <LOGOUT /> */}
        </div>
    );
};

export default AdminDashboard;
