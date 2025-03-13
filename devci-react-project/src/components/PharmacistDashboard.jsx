import { useState, useEffect } from "react";

const PharmacistDashboard = () => {
  const [doctorID, setDoctorID] = useState("");
  const [patientName, setPatientName] = useState("");
  const [medicine, setMedicine] = useState("");
  const [statusMessage, setStatusMessage] = useState("");
  const [auditLogs, setAuditLogs] = useState([]);

  const specialists = ["Cardiologist", "Neurologist", "Oncologist"]; // Allowed specializations

  const verifyPrescription = () => {
    const randomSpecialization =
      ["General Practitioner", "Dentist", "Surgeon" ,"Dermatologist", "Pedeatrician", "Dentist", "Optician"][Math.floor(Math.random() * 3)];

    let status;
    if (specialists.includes(randomSpecialization)) {
      status = "Valid ";
      setStatusMessage(`Prescription Verified Successfully.`);
    } else {
      status = "Warning";
      setStatusMessage(
        `${medicine} is not typically prescribed by a ${randomSpecialization}.`
      );
    }

    const newLog = {
      time: new Date().toLocaleString(),
      medication: medicine,
      status,
    };

    const updatedLogs = [newLog, ...auditLogs].slice(0, 10); // Keep only the last 10 logs
    setAuditLogs(updatedLogs);
    localStorage.setItem("auditLogs", JSON.stringify(updatedLogs)); // Persist logs
  };

  useEffect(() => {
    const storedLogs = JSON.parse(localStorage.getItem("auditLogs")) || [];
    setAuditLogs(storedLogs);
  }, []);

  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-4">Pharmacist Dashboard</h2>

      <div className="mb-4">
        <label className="block text-sm font-medium">Doctor's ID:</label>
        <input
          type="text"
          value={doctorID}
          onChange={(e) => setDoctorID(e.target.value)}
          className="border rounded w-full p-2"
        />
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium">Patient's Name:</label>
        <input
          type="text"
          value={patientName}
          onChange={(e) => setPatientName(e.target.value)}
          className="border rounded w-full p-2"
        />
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium">Medicine:</label>
        <input
          type="text"
          value={medicine}
          onChange={(e) => setMedicine(e.target.value)}
          className="border rounded w-full p-2"
        />
      </div>

      <button
        onClick={verifyPrescription}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
      >
        Verify Prescription
      </button>

      {statusMessage && (
        <div className={`mt-4 p-2 rounded text-white ${statusMessage.includes("⚠️") ? "bg-yellow-500" : "bg-green-500"}`}>
          {statusMessage}
        </div>
      )}

      {/* Audit Logs */}
      <h3 className="text-lg font-semibold mt-6">Audit Logs</h3>
      <ul className="mt-2 bg-gray-100 p-4 rounded-md">
        {auditLogs.length === 0 ? (
          <p className="text-gray-500">No logs available</p>
        ) : (
          auditLogs.map((log, index) => (
            <li key={index} className="border-b p-2">
              <strong>{log.time}</strong> - {log.medication} - <span className={`${log.status.includes("⚠️") ? "text-yellow-600" : "text-green-600"}`}>{log.status}</span>
            </li>
          ))
        )}
      </ul>
    </div>
  );
};

export default PharmacistDashboard;
