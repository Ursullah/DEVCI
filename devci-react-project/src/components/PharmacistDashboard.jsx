import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios"; // Import Axios

const PharmacistDashboard = () => {
  const navigate = useNavigate();
  const [search, setSearch] = useState("");
  const [doctorID, setDoctorID] = useState("");
  const [medicine, setMedicine] = useState("");
  const [statusMessage, setStatusMessage] = useState("");
  const [prescriptions, setPrescriptions] = useState([]);
  const [auditLogs, setAuditLogs] = useState([]);

  // Fetch prescriptions and audit logs from the backend
  useEffect(() => {
    const fetchPrescriptions = async () => {
      try {
        const response = await axios.get("http://localhost:5000/prescriptions/search/patient", {
          params: { name: search },
          withCredentials: true
        });
        setPrescriptions(response.data.prescriptions);
      } catch (error) {
        console.error("Error fetching prescriptions:", error.response ? error.response.data : error.message);
      }
    };

    const fetchAuditLogs = async () => {
      try {
        const response = await axios.get("http://localhost:5000/prescriptions/audit", { withCredentials: true });
        setAuditLogs(response.data.logs);
      } catch (error) {
        console.error("Error fetching audit logs:", error.response ? error.response.data : error.message);
      }
    };

    fetchPrescriptions();
    fetchAuditLogs();
  }, [search]); // Add search as a dependency to re-fetch prescriptions when search changes

  // Handle prescription verification
  const handleVerify = async () => {
    try {
      const response = await axios.post(
        "http://localhost:5000/prescriptions/verify",
        { doctor_name: doctorID, medication: medicine },
        { withCredentials: true }
      );
      setStatusMessage(response.data.message);
    } catch (error) {
      setStatusMessage("Error verifying prescription");
      console.error(error);
    }
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <div className="max-w-lg mx-auto bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-center mb-4">Pharmacist Dashboard</h2>

        {/* Search bar */}
        <div className="mb-4">
          <input
            type="text"
            placeholder="Search patient by name..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full p-2 border rounded"
          />
        </div>

        {/* Prescription list */}
        <div className="bg-white p-4 shadow rounded mb-6">
          <h3 className="text-lg font-semibold">Prescription</h3>
          {prescriptions.length === 0 ? (
            <p>{search ? "No matching patient found." : "No prescriptions available."}</p>
          ) : (
            prescriptions.map((prescription) => (
              <div key={prescription.id} className="p-3 border-b">
                <p><strong>Patient:</strong> {prescription.patient_name}</p>
                <p><strong>Medication:</strong> {prescription.medication}</p>
                <p><strong>Dosage:</strong> {prescription.dosage}</p>
                <p><strong>Doctor:</strong> {prescription.doctor_name}</p>
                <p><strong>Status:</strong> {prescription.status}</p>
              </div>
            ))
          )}
        </div>

        {/* Prescription verification section */}
        <h3 className="text-lg font-semibold mb-2">Verify prescription</h3>
        <form className="space-y-4">
          <input 
            type="text" 
            placeholder="Doctor ID"
            value={doctorID} 
            onChange={(e) => setDoctorID(e.target.value)} 
            className="w-full p-2 border rounded" 
            required 
          />

          <input 
            type="text" 
            placeholder="Medicine" 
            value={medicine} 
            onChange={(e) => setMedicine(e.target.value)} 
            className="w-full p-2 border rounded" 
            required 
          />

          <button 
            type="button" 
            onClick={handleVerify} 
            className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600">Verify Prescription</button>
        </form>
        <p className="text-center mt-4 text-red-600 font-semibold">{statusMessage}</p>
      </div>
      
      {/* Audit Log Section */}
      <div className="max-w-lg mx-auto mt-6 bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold mb-2">Audit Log</h3>
        <ul className="bg-gray-50 p-4 rounded-md">
          {auditLogs.length === 0 ? (
            <p className="text-gray-500">No logs available</p>
          ) : (
            auditLogs.map((log, index) => (
              <li key={index} className="border-b py-2">
                <strong>{log.medicine}</strong> - {log.status} on {log.created_at}
              </li>
            ))
          )}
        </ul>
      </div>
      
      {/* Back to Home Button */}
      <div className="text-center mt-6">
        <button onClick={() => navigate("/")} className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition">Back to Home</button>
      </div>
    </div>
  );
};

export default PharmacistDashboard;
