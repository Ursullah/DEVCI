import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
// import LOGOUT from "./LOGOUT";

const doctors = [
  { id: "D001", name: "Dr. John Smith", specialization: "Cardiologist", medicines: ["Aspirin", "Metoprolol", "Atorvastatin"] },
  { id: "D002", name: "Dr. Sarah Johnson", specialization: "Neurologist", medicines: ["Gabapentin", "Carbamazepine", "Dopamine"] },
  { id: "D003", name: "Dr. Emily Brown", specialization: "Oncologist", medicines: ["Tamoxifen", "Cisplatin", "Methotrexate"] },
  { id: "D004", name: "Dr. Mark Wilson", specialization: "General Practitioner", medicines: ["Paracetamol", "Ibuprofen", "Amoxicillin"] }
];

const PharmacistDashboard = () => {
  const navigate = useNavigate();
  const [prescriptions, setPrescriptions] = useState([]);
  const [search, setSearch] = useState("")
  const [doctorID, setDoctorID] = useState("");
  const [medicine, setMedicine] = useState("");
  const [statusMessage, setStatusMessage] = useState("");
  const [auditLogs, setAuditLogs] = useState([]);

  //fetch prescription from backend
  useEffect(() =>{
    fetch("http://localhost:5000/prescriptions")
      .then((res) => res.json())
      .then((data) => {setPrescriptions(data)

      })
      .catch((error) => console.error("Error fetching presciptions:", error));
    },[]);
   
    //filter prescriptions based on search
    const filteredPrescriptions = prescriptions.filter((prescription) =>
    prescription.patientName.toLowerCase().includes(search.toLowerCase())
  );
  
  const handleVerify = async () => {
    const doctor = doctors.find(doc => doc.id === doctorID);

    if (!doctor) {
      setStatusMessage("Doctor not found!");
      return;
    }

    if (!doctor.medicines.includes(medicine)) {
      setStatusMessage(`${medicine} is not typically prescribed by a ${doctor.specialization}.`);
      return;
    }

    try {
      const response = await fetch(`https://api.fda.gov/drug/label.json?search=openfda.brand_name:${medicine}`);
      const data = await response.json();

      if (data.results && data.results.length > 0) {
        setStatusMessage("Medicine is Available & Verified!");
      } else {
        setStatusMessage("Medicine is not available!");
      }
    } catch {
      setStatusMessage("API request failed!");
    }

    // Log the prescription verification
    const newLog = {
      time: new Date().toLocaleString(),
      doctor: doctor.name,
      medication: medicine,
      status: statusMessage
    };
    setAuditLogs(prevLogs => [newLog, ...prevLogs]);
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
          {prescriptions.length === 0 ?(
            <p>No prescriptions available.</p>
          ) : (
            filteredPrescriptions.map((prescription) => (
              <div key={prescription._id} className="p-3 border-b">
                 <p><strong>Patient:</strong> {prescription.patientName}</p>
                <p><strong>Age:</strong> {prescription.patientAge}</p>
                <p><strong>Contact:</strong> {prescription.info}</p>
                <p><strong>Medication:</strong> {prescription.medication}</p>
                <p><strong>Dosage:</strong> {prescription.dosage}</p>
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
           className="w-full p-2 border rounded" required />

          <input 
          type="text" 
          placeholder="Medicine" 
          value={medicine} 
          onChange={e => setMedicine(e.target.value)} 
          className="w-full p-2 border rounded" required />

          <button 
          type="button" 
          onClick={handleVerify} 
          className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600">Verify Prescription</button>
        </form>
        <p className="text-center mt-4 text-red-600 font-semibold">{statusMessage}</p>
      </div>
      
      {/* Audit Log Section */}
      <div className="max-w-lg mx-auto mt-6 bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold mb-2">Audit Logs</h3>
        <ul className="bg-gray-50 p-4 rounded-md">
          {auditLogs.length === 0 ? (
            <p className="text-gray-500">No logs available</p>
          ) : (
            auditLogs.map((log, index) => (
              <li key={index} className="border-b py-2">
                <strong>{log.time}</strong> - {log.doctor} prescribed {log.medication} - <span className="text-blue-600">{log.status}</span>
              </li>
            ))
          )}
        </ul>
      </div>
      
      {/* Back to Home Button */}
      <div className="text-center mt-6">
        <button onClick={() => navigate("/")} className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition">Back to Home</button>
      </div>
      {/* <LOGOUT /> */}
    </div>
  );
};

export default PharmacistDashboard;