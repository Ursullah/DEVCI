import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";

const LogIn = ({ setIsAuthenticated }) => {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [rememberMe, setRememberMe] = useState(false);
    const [errors, setErrors] = useState({});
    const [role, setRole] = useState(""); // Role state added
    const navigate = useNavigate();

    const validate = () => {
        const validationErrors = {};
        if (!username) {
            validationErrors.username = "Username is required";
        }
        if (!email) {
            validationErrors.email = "Email is required";
        } else if (!/\S+@\S+\.\S+/.test(email)) {
            validationErrors.email = "Invalid email format";
        }
        if (!password) {
            validationErrors.password = "Password is required";
        } else if (password.length < 8) {
            validationErrors.password = "Password should be at least 8 characters long";
        }
        if (!role) {
            validationErrors.role = "Role selection is required";
        }

        setErrors(validationErrors);
        return Object.keys(validationErrors).length === 0;
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        if (name === "username") setUsername(value);
        else if (name === "email") setEmail(value);
        else if (name === "password") setPassword(value);
    };

    const handleLogin = (e) => {
        e.preventDefault(); // Prevent form submission
        if (!validate()) return; // Stop execution if validation fails

        console.log("Selected Role:", role);

        setIsAuthenticated(true);
        localStorage.setItem("auth", "true");
        localStorage.setItem("role", role); // Store role in localStorage
        
        if (role === "Doctor") {
            navigate("/doctor-dashboard");
        } else if (role === "Pharmacist") {
            navigate("/pharmacist-dashboard");
        } else if (role === "Admin") {
            navigate("/admin-dashboard");
        } else {
            navigate("/home");
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <div className="w-full max-w-md p-6 bg-white rounded-lg shadow-lg">
                <h2 className="text-2xl font-bold text-center text-gray-700">LOGIN</h2>

                <form onSubmit={handleLogin} className="mt-4">
                    <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-600">Username:</label>
                        <input
                            className="border rounded w-full py-2 px-3"
                            type="text"
                            name="username"
                            value={username}
                            onChange={handleChange}
                            placeholder="Enter username"
                        />
                        {errors.username && <span className="text-red-500 text-xs italic">{errors.username}</span>}
                    </div>

                    <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-600">Email:</label>
                        <input
                            className="border rounded w-full py-2 px-3"
                            type="text"
                            name="email"
                            value={email}
                            onChange={handleChange}
                            placeholder="example@email.com"
                        />
                        {errors.email && <span className="text-red-500 text-xs italic">{errors.email}</span>}
                    </div>

                    <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-600">Password:</label>
                        <input
                            className="border rounded w-full py-2 px-3"
                            type="password"
                            name="password"
                            value={password}
                            onChange={handleChange}
                            placeholder="********"
                        />
                        {errors.password && <span className="text-red-500 text-xs italic">{errors.password}</span>}
                    </div>

                    {/* Role Selection Dropdown */}
                    <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-600">Select Role:</label>
                        <select
                            className="border rounded w-full py-2 px-3"
                            value={role}
                            onChange={(e) => setRole(e.target.value)}
                        >
                            <option value="">Select Role</option>
                            <option value="Doctor">Doctor</option>
                            <option value="Pharmacist">Pharmacist</option>
                            <option value="Admin">Admin</option>
                        </select>
                        {errors.role && <span className="text-red-500 text-xs italic">{errors.role}</span>}
                    </div>

                    <div className="flex items-center justify-between mb-4">
                        <label className="flex items-center text-sm">
                            <input
                                type="checkbox"
                                className="mr-2"
                                checked={rememberMe}
                                onChange={() => setRememberMe(!rememberMe)}
                            />
                            Remember me
                        </label>
                        <a href="#" className="text-sm text-blue-500 hover:underline">
                            Forgot password?
                        </a>
                    </div>

                    <button
                        className="bg-indigo-500 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded"
                        type="submit"
                    >
                        Log in
                    </button>
                </form>
            </div>
        </div>
    );
};

export default LogIn;
