import React, { useState, useEffect } from "react";
import axios from "axios";
import LOGOUT from "../components/LOGOUT";
import { Modal, Form, Input, Button, message } from 'antd';

const AdminDashboard = () => {
  const [doctors, setDoctors] = useState([]);
  const [formData, setFormData] = useState({
    name: "",
    hospital: "",
    specialization: "",
    username: "",
    password: "",
    confirmPassword: "",
  });
  const [errors, setErrors] = useState({});
  const [editingDoctor, setEditingDoctor] = useState(null);
  const [auditLogs, setAuditLogs] = useState([]);
  const [prescriptions, setPrescriptions] = useState([]);
  const [showEditModal, setShowEditModal] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [doctorsRes, auditRes, prescriptionsRes] = await Promise.all([
          axios.get("http://localhost:5000/api/getdoctors"),
          axios.get("http://127.0.0.1:5000/api/adminprescription"),
          axios.get("http://localhost:5000/api/adminprescription"),
        ]);

        setDoctors(doctorsRes.data);
        console.log(doctors)
        setAuditLogs(auditRes.data);
        setPrescriptions(prescriptionsRes.data);
      } catch (err) {
        console.error("Error fetching data:", err);
        setErrors({ message: "Error fetching data. Please try again." });
      }
    };

    fetchData();
  }, []);

  const validate = () => {
    const validationErrors = {};
    if (!formData.name) validationErrors.name = "Doctor's name is required";
    if (!formData.hospital)
      validationErrors.hospital = "Hospital name is required";
    if (!formData.specialization)
      validationErrors.specialization = "Specialization is required";
    if (!formData.username) validationErrors.username = "Username is required";
    if (!formData.password) validationErrors.password = "Password is required";
    if (formData.password !== formData.confirmPassword)
      validationErrors.confirmPassword = "Passwords do not match";
    if (formData.password.length < 8)
      validationErrors.password = "Password must be at least 8 characters long";

    setErrors(validationErrors);
    return Object.keys(validationErrors).length === 0;
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    const doctorData = {
      username: formData.username,
      password: formData.password,
      full_name: formData.name,
      hospital: formData.hospital,
      specialization: formData.specialization,
    };

    try {
      if (editingDoctor !== null) {
        await axios.put(
          `http://localhost:5000/api/editdoctor/${editingDoctor}`,
          doctorData
        );
        setDoctors(
          doctors.map((doc) =>
            doc.id === editingDoctor ? { ...doc, ...doctorData } : doc
          )
        );
        alert("Doctor updated successfully!");
      } else {
        const response = await axios.post(
          "http://localhost:5000/api/register-doctors",
          doctorData
        );
        setDoctors([...doctors, response.data]);
        alert("Doctor registered successfully!");
      }

      // Reset form and state
      setFormData({
        name: "",
        hospital: "",
        specialization: "",
        username: "",
        password: "",
        confirmPassword: "",
      });
      setEditingDoctor(null);
      setShowEditModal(false);
    } catch (error) {
      console.error("Error saving doctor:", error);
    }
  };

  const handleDelete = async (doctorId) => {
    if (!window.confirm("Are you sure you want to delete this doctor?")) return;

    try {
      await axios.delete(`http://localhost:5000/api/deletedoctor/${doctorId}`);
      setDoctors(doctors.filter((doc) => doc.id !== doctorId));
      alert("Doctor deleted successfully!");
    } catch (error) {
      console.error("Error deleting doctor:", error);
    }
  };

  const handleEdit = (doctor) => {
    setFormData({
      name: doctor.full_name,
      hospital: doctor.hospital,
      specialization: doctor.specialization,
      username: doctor.username || "",
      password: "",
      confirmPassword: "",
    });
    setEditingDoctor(doctor.id);
    setShowEditModal(true);
  };

  const adminName = localStorage.getItem("name");

  return (
    <div className="flex flex-col min-h-screen bg-gray-100 p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">ADMIN'S DASHBOARD</h1>
        <div className="flex items-center gap-4">
          <h2 className="text-xl font-semibold">Hello {adminName}</h2>
          <LOGOUT />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 ">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-lg font-bold mb-4">Register New Doctor</h2>
          <button
            onClick={() => {
              setEditingDoctor(null);
              setShowEditModal(true);
              setFormData({
                name: "",
                hospital: "",
                specialization: "",
                username: "",
                password: "",
                confirmPassword: "",
              });
            }}
            className="bg-indigo-500 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded w-full mb-4"
          >
            Add New Doctor
          </button>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md col-span-1 overflow-y-scroll h-screen">
          <h2 className="text-lg font-bold mb-4">Registered Doctors</h2>
          {doctors.length === 0 ? (
            <p className="text-gray-500">No doctors registered.</p>
          ) : (
            <ul className="space-y-3">
              {doctors.map((doctor) => (
                <li key={doctor.id} className="border-b pb-3">
                  <div className="flex justify-between items-start">
                    <div>
                      <p>
                        <strong>Name:</strong> {doctor.doctorName}
                      </p>
                      <p>
                        <strong>Hospital:</strong> {doctor.hospital}
                      </p>
                      <p>
                        <strong>Specialization:</strong> {doctor.specialization}
                      </p>
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleEdit(doctor)}
                        className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-700"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(doctor.id)}
                        className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-700"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md col-span-1 h-screen overflow-y-scroll">
          <h2 className="text-lg font-bold mb-4">Pharmacist Audit Logs</h2>
          {auditLogs.length === 0 ? (
            <p className="text-gray-500">No audit logs available.</p>
          ) : (
            <ul className="space-y-3">
              {auditLogs.map((log, index) => (
                <li key={index} className="border-b pb-3">
                  <p>
                    <strong>Pharmacist:</strong>{" "}
                    {log.pharmacist?.pharmacistName || "Unassigned"}
                  </p>
                  <p>
                    <strong>Medication Issued:</strong> {log.medicine_name}
                  </p>
                  <p>
                    <strong>Status:</strong> {log.status}
                  </p>
                  <p>
                    <strong>Time:</strong>{" "}
                    {new Date(log.updated_at).toLocaleString()}
                  </p>
                </li>
              ))}
            </ul>
          )}
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md col-span-1 max-h-96 overflow-y-auto">
          <h2 className="text-lg font-bold mb-4">Doctors' Prescriptions</h2>
          {prescriptions.length === 0 ? (
            <p className="text-gray-500">No prescriptions available.</p>
          ) : (
            <ul className="space-y-3">
              {prescriptions.map((prescription, index) => (
                <li key={index} className="border-b pb-3">
                  <p>
                    <strong>Patient:</strong> {prescription.patient_name}
                  </p>
                  <p>
                    <strong>Medication:</strong> {prescription.medicine_name}
                  </p>
                  <p>
                    <strong>Dosage:</strong> {prescription.dosage}
                  </p>
                  <p>
                    <strong>Status:</strong> {prescription.status}
                  </p>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      {showEditModal && (
        <Modal
          title={editingDoctor !== null ? "Edit Doctor" : "Register Doctor"}
          visible={showEditModal}
          onCancel={() => setShowEditModal(false)}
          footer={[
            <Button key="back" onClick={() => setShowEditModal(false)}>
              Cancel
            </Button>,
            <Button key="submit" type="primary" onClick={handleSubmit}>
              {editingDoctor !== null ? "Update" : "Register"}
            </Button>,
          ]}
          width={600}
        >
          <Form layout="vertical">
            <Form.Item
              label="Doctor's Name"
              validateStatus={errors.name ? "error" : ""}
              help={errors.name}
            >
              <Input
                name="name"
                value={formData.name}
                onChange={handleInputChange}
              />
            </Form.Item>

            <Form.Item
              label="Hospital"
              validateStatus={errors.hospital ? "error" : ""}
              help={errors.hospital}
            >
              <Input
                name="hospital"
                value={formData.hospital}
                onChange={handleInputChange}
              />
            </Form.Item>

            <Form.Item
              label="Specialization"
              validateStatus={errors.specialization ? "error" : ""}
              help={errors.specialization}
            >
              <Input
                name="specialization"
                value={formData.specialization}
                onChange={handleInputChange}
              />
            </Form.Item>

            <Form.Item
              label="Username"
              validateStatus={errors.username ? "error" : ""}
              help={errors.username}
            >
              <Input
                name="username"
                value={formData.username}
                onChange={handleInputChange}
              />
            </Form.Item>

            <Form.Item
              label="Password"
              validateStatus={errors.password ? "error" : ""}
              help={errors.password}
            >
              <Input.Password
                name="password"
                value={formData.password}
                onChange={handleInputChange}
              />
            </Form.Item>

            <Form.Item
              label="Confirm Password"
              validateStatus={errors.confirmPassword ? "error" : ""}
              help={errors.confirmPassword}
            >
              <Input.Password
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleInputChange}
              />
            </Form.Item>
          </Form>
        </Modal>
      )}
    </div>
  );
};

export default AdminDashboard;
