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
        const response = await axios.get("http://localhost:5000/prescriptions/doctor", { withCredentials: true });
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
  }, []);

  // Filter prescriptions based on search
  const filteredPrescriptions = prescriptions.filter((prescription) =>
    prescription.patient_name.toLowerCase().includes(search.toLowerCase())
  );

  const handleVerify = async () => {
    // Verification logic remains the same
    // ...
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
          {filteredPrescriptions.length === 0 ? (
            search ? (
              <p>No matching patient found.</p>
            ) : (
              <p>No prescriptions available.</p>
            )
          ) : (
            filteredPrescriptions.map((prescription) => (
              <div key={prescription.id} className="p-3 border-b">
                <p><strong>Patient:</strong> {prescription.patient_name}</p>
                <p><strong>Age:</strong> {prescription.patient_age}</p>
                <p><strong>Contact:</strong> {prescription.info}</p>
                <p><strong>Medication:</strong> {prescription.medication}</p>
                <p><strong>Dosage:</strong> {prescription.dosage}</p>
                <p><strong>Doctor:</strong> {prescription.doctor_name}</p>
              </div>
            ))
          )}
        </div>

        {/* Verification section */}
        <h3 className="text-lg font-semibold mb-2">Verify prescription</h3>
        <form className="space-y-4">
          <input 
            type="text" 
            placeholder="Doctor ID"
            value={doctorID} 
            onChange={e => setDoctorID(e.target.value)} 
            className="w-full p-2 border rounded" required 
          />

          <input 
            type="text" 
            placeholder="Medicine" 
            value={medicine} 
            onChange={e => setMedicine(e.target.value)} 
            className="w-full p-2 border rounded" required 
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
        <h3 className="text-lg font-semibold mb-2">Doctor's Log</h3>
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