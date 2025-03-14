import { useState, useEffect } from "react";

const PharmacistDashboard = () => {
  const [doctorID, setDoctorID] = useState("");
  const [patientName, setPatientName] = useState("");
  const [medicine, setMedicine] = useState("");
  const [statusMessage, setStatusMessage] = useState("");
  const [auditLogs, setAuditLogs] = useState([]);
  const [apiStatus, setApiStatus] = useState(null);

  // Specializations that are allowed to prescribe
  const specialists = ["Cardiologist", "Neurologist", "Oncologist"];

  const verifyPrescription = async () => {
    const randomSpecialization =
      ["General Practitioner", "Dentist", "Surgeon", "Dermatologist", "Pediatrician", "Optician"][
        Math.floor(Math.random() * 6)
      ];

    let status;
    let warningMessage = "";

    // Check if the specialization is valid
    if (!specialists.includes(randomSpecialization)) {
      status = "Warning";
      warningMessage = `${medicine} is not typically prescribed by a ${randomSpecialization}.`;
    } else {
      status = "Valid";
      warningMessage = "Prescription Verified Successfully.";
    }

    setStatusMessage(warningMessage);

    // Check medicine availability via API
    try {
      const response = await fetch(`https://api.example.com/medicines?name=${medicine}`);
      const data = await response.json();

      if (response.ok) {
        if (data.available) {
          setApiStatus({ type: "valid", message: "Medicine is Available!" });
        } else {
          setApiStatus({ type: "error", message: "Medicine is not Available!" });
        }
      } else {
        setApiStatus({ type: "error", message: "Error fetching data!" });
      }
    } catch (error) {
      setApiStatus({ type: "error", message: " API request failed!" });
    }

    // Store in audit logs
    const newLog = {
      time: new Date().toLocaleString(),
      medication: medicine,
      status: status === "Warning" ? "⚠️ Warning" : "Valid",
    };

    const updatedLogs = [newLog, ...auditLogs].slice(0, 10); // Keep only last 10 logs
    setAuditLogs(updatedLogs);
    localStorage.setItem("auditLogs", JSON.stringify(updatedLogs)); // Persist logs
  };

  // Load audit logs from local storage
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

      {/* Specialization Warning/Success */}
      {statusMessage && (
        <div className={`mt-4 p-2 rounded text-white ${statusMessage.includes("⚠️") ? "bg-yellow-500" : "bg-green-500"}`}>
          {statusMessage}
        </div>
      )}

      {/* API Medicine Availability Status */}
      {apiStatus && (
        <p className={`mt-2 text-${apiStatus.type === "valid" ? "green" : "red"}-500`}>
          {apiStatus.message}
        </p>
      )}

      {/* Audit Logs */}
      <h3 className="text-lg font-semibold mt-6">Audit Logs</h3>
      <ul className="mt-2 bg-gray-100 p-4 rounded-md">
        {auditLogs.length === 0 ? (
          <p className="text-gray-500">No logs available</p>
        ) : (
          auditLogs.map((log, index) => (
            <li key={index} className="border-b p-2">
              <strong>{log.time}</strong> - {log.medication} -{" "}
              <span className={log.status.includes("⚠️") ? "text-yellow-600" : "text-green-600"}>
                {log.status}
              </span>
            </li>
          ))
        )}
      </ul>
    </div>
  );
};

export default PharmacistDashboard;
