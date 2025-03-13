import { useEffect, useState } from "react";
import PharmacistDashboard from "./PharmacistDashboard";

const HomePage = ({ setIsAuthenticated }) => {
  const [selectedRole, setSelectedRole] = useState("");

  useEffect(() => {
    const role = localStorage.getItem("role") || "Guest";
    console.log("User Role:", role);
    setSelectedRole(role);
  }, [setSelectedRole]);

  return (
    <div
      className="relative w-full min-h-screen bg-cover bg-center bg-no-repeat pt-16"
      style={{ backgroundImage: "url('/assets/prescription.jpg')" }}
    >
      <div className="max-w-5xl text-black p-12">
        <h2 className="text-3xl mt-6 font-bold">Here to provide your medicine solution!</h2>
        <p className="text-lg mt-2 leading-relaxed p-2">
          Prescription verification ensures your safety by confirming the accuracy of your medication, dosage, and
          potential drug interactions. It helps prevent errors, allergies, and misuse while complying with medical and
          legal guidelines. This process also protects against fraud and ensures you receive the right treatment.
          Verifying prescriptions is essential for safe and effective healthcare.
        </p>

        <button
          type="button"
          className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition duration-300 cursor-pointer mt-4"
        >
          See Medicine Available
        </button>
      </div>
    </div>
  );
};

export default HomePage;
