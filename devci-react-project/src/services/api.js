// src/services/api.js
import axios from 'axios';

const API_URL = 'http://localhost:5000';

// Create axios instance with credentials support
const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Authentication services
export const authService = {
  login: async (email, password) => {
    try {
      const response = await api.post('/login', { email, password });
      return response.data;
    } catch (error) {
      throw error.response ? error.response.data : new Error('Network error');
    }
  },
  
  register: async (userData) => {
    try {
      const response = await api.post('/register', userData);
      return response.data;
    } catch (error) {
      throw error.response ? error.response.data : new Error('Network error');
    }
  },
  
  logout: async () => {
    try {
      const response = await api.post('/logout');
      return response.data;
    } catch (error) {
      throw error.response ? error.response.data : new Error('Network error');
    }
  },
  
  getCurrentUser: async () => {
    try {
      const response = await api.get('/user');
      return response.data;
    } catch (error) {
      return null; // User not logged in
    }
  }
};

// Prescription services
export const prescriptionService = {
  // For doctors
  createPrescription: async (prescriptionData) => {
    try {
      const response = await api.post('/prescriptions', prescriptionData);
      return response.data;
    } catch (error) {
      throw error.response ? error.response.data : new Error('Network error');
    }
  },
  
  getDoctorPrescriptions: async () => {
    try {
      const response = await api.get('/prescriptions/doctor');
      return response.data;
    } catch (error) {
      throw error.response ? error.response.data : new Error('Network error');
    }
  },
  
  // For pharmacists
  verifyPrescription: async (verificationData) => {
    try {
      const response = await api.post('/prescriptions/verify', verificationData);
      return response.data;
    } catch (error) {
      throw error.response ? error.response.data : new Error('Network error');
    }
  },
  
  searchPrescriptionsByPatient: async (patientName) => {
    try {
      const response = await api.get(`/prescriptions/search/patient?name=${encodeURIComponent(patientName)}`);
      return response.data;
    } catch (error) {
      throw error.response ? error.response.data : new Error('Network error');
    }
  },
  
  searchPrescriptionById: async (id) => {
    try {
      const response = await api.get(`/prescriptions/search/id/${id}`);
      return response.data;
    } catch (error) {
      throw error.response ? error.response.data : new Error('Network error');
    }
  },
  
  getAuditLog: async () => {
    try {
      const response = await api.get('/prescriptions/audit');
      return response.data;
    } catch (error) {
      throw error.response ? error.response.data : new Error('Network error');
    }
  }
};

// Admin services
export const adminService = {
  getDoctors: async () => {
    try {
      const response = await api.get('/admin/doctors');
      return response.data;
    } catch (error) {
      throw error.response ? error.response.data : new Error('Network error');
    }
  },
  
  registerDoctor: async (doctorData) => {
    try {
      const response = await api.post('/admin/doctors', doctorData);
      return response.data;
    } catch (error) {
      throw error.response ? error.response.data : new Error('Network error');
    }
  },
  
  updateDoctor: async (id, doctorData) => {
    try {
      const response = await api.put(`/admin/doctors/${id}`, doctorData);
      return response.data;
    } catch (error) {
      throw error.response ? error.response.data : new Error('Network error');
    }
  },
  
  deleteDoctor: async (id) => {
    try {
      const response = await api.delete(`/admin/doctors/${id}`);
      return response.data;
    } catch (error) {
      throw error.response ? error.response.data : new Error('Network error');
    }
  }
};