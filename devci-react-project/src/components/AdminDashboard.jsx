// AdminDashboard.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import LOGOUT from '../components/LOGOUT'; // Assuming LOGOUT is a component for logging out

const AdminDashboard = () => {
    const [doctors, setDoctors] = useState([]);
    const [name, setName] = useState("");
    const [hospital, setHospital] = useState("");
    const [specialization, setSpecialization] = useState("");
    const [errors, setErrors] = useState({});
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [editingDoctor, setEditingDoctor] = useState(null);
    const [auditLogs, setAuditLogs] = useState([]);
    const [prescriptions, setPrescriptions] = useState([]);

    useEffect(() => {
        const fetchDoctors = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/admin/doctors', {
                    headers: {}
                });
                setDoctors(response.data.doctors);
                console.log(response.data)

            } catch (err) {
                console.error("Error fetching doctors:", err);
                setErrors({ message: "Error fetching doctors. Please try again." });
            }
        };

        const fetchAuditLogs = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:5000/api/audit-logs");
                setAuditLogs(response.data.logs);
            } catch (err) {
                console.error("Error fetching audit logs:", err);
                setErrors({ message: "Error fetching audit logs. Please try again." });
            }
        };

        const fetchPrescriptions = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:5000/api/prescriptions");
                setPrescriptions(response.data.prescriptions);
            } catch (err) {
                console.error("Error fetching prescriptions:", err);
                setErrors({ message: "Error fetching prescriptions. Please try again." });
            }
        };

        fetchDoctors();
        fetchAuditLogs();
        fetchPrescriptions();
    }, []);

    const validate = () => {
        const validationErrors = {};
        if (!name) validationErrors.name = "Doctor's name is required";
        if (!hospital) validationErrors.hospital = "Hospital name is required";
        if (!specialization) validationErrors.specialization = "Specialization is required";
        if (!username) validationErrors.username = "Username is required";
        if (!password) validationErrors.password = "Password is required";
        if (password !== confirmPassword) validationErrors.confirmPassword = "Passwords do not match";
        if (password.length < 8) validationErrors.password = "Password must be at least 8 characters long";

        setErrors(validationErrors);
        return Object.keys(validationErrors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!validate()) return;

        const doctorData = { 
            username,
            password,
            full_name: name,
            hospital, 
            specialization };

        try {
            if (editingDoctor !== null) {
                // Update existing doctor
                await axios.put(`http://127.0.0.1:5000/admin/doctors/${editingDoctor}`, doctorData);
                setDoctors(doctors.map(doc => doc.id === editingDoctor ? { ...doc, ...doctorData } : doc));
                alert("Doctor updated successfully!");
            } else {
                // Register new doctor
                const response = await axios.post("http://localhost:5000/api/admin/register-doctors", doctorData);
                setDoctors([...doctors, response.data]);
                alert("Doctor registered successfully!");
            }

            // Clear form fields
            setName("");
            setHospital("");
            setUsername("");
            setPassword("");
            setConfirmPassword("");
            setSpecialization("");
            setEditingDoctor(null);
        } catch (error) {
            console.error("Error saving doctor:", error);
        }
    };

    const handleDelete = async (doctorId) => {
        if (!window.confirm("Are you sure you want to delete this doctor?")) return;

        try {
            await axios.delete(`http://127.0.0.1:5000/api/admin/doctors/${doctorId}`);
            setDoctors(doctors.filter(doc => doc.id !== doctorId));
            alert("Doctor deleted successfully!");
        } catch (error) {
            console.error("Error deleting doctor:", error);
        }
    };

    const handleEdit = (doctor) => {
        setName(doctor.name);
        setEmail(doctor.email);
        setHospital(doctor.hospital);
        setSpecialization(doctor.specialization);
        setEditingDoctor(doctor.id);
    };

    return (
        <div className="flex flex-col min-h-screen bg-gray-400">
            <h1 className="text-2xl font-bold text-center mb-4">ADMIN'S DASHBOARD</h1>
            <h2 className='text-2xl font-bold mb-4'>Hello Allan!</h2>

            {/* Doctor Registration Form */}
            <div className='grid grid-cols-4  gap-4 w-full p-4'>
            <form onSubmit={handleSubmit} className="w-full max-w-2xl bg-white p-6 rounded-lg shadow-lg">
                <h2 className="text-lg font-bold mb-4">{editingDoctor !== null ? "Edit Doctor" : "Register Doctor"}</h2>

                <label className="block font-semibold">Doctor's Name:</label>
                <input type="text" name="name" value={name} onChange={(e) => setName(e.target.value)} className="w-full p-2 border border-gray-300 rounded mb-4" />
                {errors.name && <span className="text-red-500 text-xs italic">{errors.name}</span>}

                <label className="block font-semibold">Hospital:</label>
                <input type="text" name="hospital" value={hospital} onChange={(e) => setHospital(e.target.value)} className="w-full p-2 border border-gray-300 rounded mb-4" />
                {errors.hospital && <span className="text-red-500 text-xs italic">{errors.hospital}</span>}

                <label className="block font-semibold">Specialization:</label>
                <input type="text" name="specialization" value={specialization} onChange={(e) => setSpecialization(e.target.value)} className="w-full p-2 border border-gray-300 rounded mb-4" />
                {errors.specialization && <span className="text-red-500 text-xs italic">{errors.specialization}</span>}

                <label className="block font-semibold">Username:</label>
                <input type="text" name="username" value={username} onChange={(e) => setUsername(e.target.value)} className="w-full p-2 border border-gray-300 rounded mb-4" />
                {errors.username && <span className="text-red-500 text-xs italic">{errors.username}</span>}

                <label className="block font-semibold">Password:</label>
                <input type="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full p-2 border border-gray-300 rounded mb-4" />
                {errors.password && <span className="text-red-500 text-xs italic">{errors.password}</span>}

                <label className="block font-semibold">Confirm Password:</label>
                <input type="password" name="confirmPassword" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} className="w-full p-2 border border-gray-300 rounded mb-4" />
                {errors.confirmPassword && <span className="text-red-500 text-xs italic">{errors.confirmPassword}</span>}

                <button className="bg-indigo-500 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded w-full" type="submit">
                    {editingDoctor !== null ? "Update Doctor" : "Register Doctor"}
                </button>
            </form>

            {/* Doctors List */}
            <div className="w-full max-w-2xl bg-white p-6 rounded-lg shadow-lg">
                <h2 className="text-lg font-bold mb-4">Registered Doctors</h2>
                {doctors.length === 0 ? (
                    <p className="text-gray-500">No doctors registered.</p>
                ) : (
                    <ul>
                        {doctors.map((doctor) => (
                            <li key={doctor.id} className="flex justify-between items-center border-b py-2">
                                <div>
                                    <p><strong>Name:</strong> {doctor.full_name}</p>
                                    <p><strong>Hospital:</strong> {doctor.hospital}</p>
                                    <p><strong>Specialization:</strong> {doctor.specialization}</p>
                                </div>
                                <div>
                                    <button onClick={() => handleEdit(doctor)} className="bg-blue-500 text-white px-3 py-1 rounded mr-2 hover:bg-blue-700">Edit</button>
                                    <button onClick={() => handleDelete(doctor.id)} className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-700">Delete</button>
                                </div>
                            </li>
                        ))}
                    </ul>
                )}
            </div>

            {/* Pharmacist Audit Logs */}
            <div className="w-full max-w-2xl bg-white p-6 rounded-lg shadow-lg">
                <h2 className="text-lg font-bold mb-4">Pharmacist Audit Logs</h2>
                {auditLogs.length === 0 ? (
                    <p className="text-gray-500">No audit logs available.</p>
                ) : (
                    <ul>
                        {auditLogs.map((log) => (
                            <li key={log.id} className="border-b py-2">
                                <p><strong>Pharmacist:</strong> {log.pharmacistName}</p>
                                <p><strong>Medication Issued:</strong> {log.medication}</p>
                                <p><strong>Transaction Status:</strong> {log.status}</p>
                                <p><strong>Time:</strong> {log.time}</p>
                            </li>
                        ))}
                    </ul>
                )}
            </div>

            {/* Doctors' Prescriptions */}
            <div className="w-full max-w-2xl bg-white p-6 rounded-lg shadow-lg">
                <h2 className="text-lg font-bold mb-4">Doctors' Prescriptions</h2>
                {prescriptions.length === 0 ? (
                    <p className="text-gray-500">No prescriptions available.</p>
                ) : (
                    <ul>
                        {prescriptions.map((prescription) => (
                            <li key={prescription.id} className="border-b py-2">
                                <p><strong>Patient Name:</strong> {prescription.patientName}</p>
                                <p><strong>Medication:</strong> {prescription.medicine}</p>
                                <p><strong>Dosage:</strong> {prescription.dosage}</p>
                                <p><strong>Status:</strong> {prescription.status}</p>   
                            </li>
                        ))}
                        
                    </ul>
                )}
            </div>
        </div>
        </div>
    );
    <LOGOUT />
};

export default AdminDashboard;
