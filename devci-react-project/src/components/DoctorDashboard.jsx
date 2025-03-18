import React, { useState } from 'react'

const DoctorDashboard = () => {
    const newPrescription= {}
    const[patientName, setPatientName] = useState("");
    const[patientAge, setPatientAge] = useState("");
    const[info, setInfo] = useState("");
    const[medication, setMedication] = useState("");
    const[dosage, setDosage] = useState("")
    const[errors, setErrors] = useState("");

    const validate = () => {
        const validationErrors = {};
        if (!patientName) validationErrors.name = "Patient is required";
        if (!patientAge) validationErrors.patientAge = "Age is required";
        if (!info) validationErrors.info = "Patient contact is required";
        if(!medication) validationErrors.medication ="Enter medicine for presciption";
        if(!dosage) validationErrors.dosage = "Select dosage"
        
        setErrors(validationErrors);
        return Object.keys(validationErrors).length === 0;
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        if (name === "patientName") setPatientName(value);
        else if (name === "patientAge") setPatientAge(value);
        else if (name === "info") setInfo(value);
        else if (name === "medication") setMedication(value);
        else if (name === "dosage") setDosage(value)
    };


    const handleSubmit = (e) =>{
        e.preventDefault(); // Prevent form submission
        if (!validate()) return; // Stop execution if validation fails
        alert("Patient prescription is saved✅")
       }
    

  return (
    <>
    <div>
        <form onSubmit={handleSubmit}>
            <div>
            <label>Patient's Name:</label>
                <input 
                type="text" 
                name="patientName" 
                value={patientName}
                onChange={handleChange}
                placeholder="Enter patient's name"></input>
            </div>
            {errors.patientName && <span className="text-red-500 text-xs italic">{errors.patientName}</span>}
            <div>
                <label>Patient's age:</label>
                <input 
                type="text" 
                name="patientAge"
                value={patientAge}
                onChange={handleChange} 
                placeholder="Enter Age"></input>
            </div>
            {errors.patientAge && <span className="text-red-500 text-xs italic">{errors.patientAge}</span>}
            <div>
                <label>Contact:</label>
                    <input 
                    type="text" 
                    name="info"
                    value={info}
                    onChange={handleChange} 
                    placeholder="0700000000"></input>
            </div>
            {errors.info && <span className="text-red-500 text-xs italic">{errors.info}</span>}
            <div>
                <label>Medicine Name:</label>
                <input type="text"
                name="medication"
                value={medication}
                onChange={handleChange} 
                placeholder="Enter Medicine Name"></input>
            </div>
            {errors.medication && <span className="text-red-500 text-xs italic">{errors.medication}</span>}
            <div>
                <label>Select dosage</label>
                <select name="dosage" value={dosage} onChange={handleChange}>
                <option value="1*2">1*2</option>
                <option value="2*2">2*2</option>
                <option value="2*3">2*3</option>
                <option value="2*4">2*4</option>
                <option value="3*3">3*3</option>
                <option value="3*1">3*1</option>
                </select>
            </div>
            <button type="submit"  className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600">
                Set Prescription
            </button>
        </form>
    </div>
    </>
  )
}

export default DoctorDashboard
