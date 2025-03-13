import React from 'react'
import { useState } from 'react';
import {useNavigate} from "react-router-dom";

const LogIn = ({setIsAuthenticated}) => {

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [output, setOutput] = useState("null")
    const [rememberMe, setRememberMe] = useState(false)
    const [errors, setErrors] = useState("")
    const navigate = useNavigate();

    const Validate = (e) =>{
        const ValidationErrors = {};
        if(!username){
            ValidationErrors.username = "Username is required"
        }
        if(!email) {
            ValidationErrors.email = "Email is required"
        } else if (!/\S+@\S+\.\S+/.test(email)){
            ValidationErrors.email = "Invalid Email Format"
        }
        if(!password){
            ValidationErrors.password = "Password is required"
        } else if(password.length < 8){
            ValidationErrors.password = "Password should be atleast 8 chars long"
        }

        setErrors(ValidationErrors);
        return Object.keys(ValidationErrors).length === 0;
    };

    const handleChange = (e) =>{
        const {name, value} = e.target;
        if(name === "username") setUsername(value);
        else if(name === "email") setEmail(value);
        else if(name === "password") setPassword(value);
    };

        const handleLogin = (e) =>{
            e.preventDefault();
            if(Validate()) {
                setIsAuthenticated(true);
                localStorage.setItem("auth", "true");
                navigate("/home");
            }
    
    };
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
     <div className="w-full max-w-md p-6 bg-white rounded-lg shadow-lg">

        <h2 className='text-2xl font-bold text-center text-gray-700'>LOGIN</h2>

        <form onSubmit={handleLogin} className='mt-4'> 
        <div className='mb-4'>
          <label className="block text-sm font-medium text-gray-600">Username:</label>
            <input className='appearance-none border border-gray-400 rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-indigo-500'  
              type="text" 
              name="username"
              value={username}
              onChange={handleChange} 
              placeholder="Enter username" />
             {errors.username && <span className='text-red-500 text-xs italic' >{errors.username}</span>}
        <br />
        </div>

        <div className='mb-4'>
          <label className="block text-sm font-medium text-gray-600">Email:</label>
            <input className='appearance-none border border-gray-400 rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-indigo-500'  
              type="text" 
              name="email" 
              value={email}
              onChange={handleChange}
              placeholder="example@email.com" />
            {errors.email && <span className='text-red-500 text-xs italic'>{errors.email}</span>}
           <br />
        </div>

        <div className='mb-4' >
         <label className="block text-sm font-medium text-gray-600" >Password:</label>
          <input className='appearance-none border border-gray-400 rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-indigo-500'  
            type="password" 
            name="password" 
            value={password}
            onChange={handleChange}
            placeholder="********" />
           {errors.password && <span className='text-red-500 text-xs italic'>{errors.password}</span>}
           <br />
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
        className='bg-indigo-500 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded focus:ouline-none focus:shadow-outline' 
        type="submit" >Log in</button>
      </form>
     </div>
    </div>
  )
}

export default LogIn
