import {BrowserRouter as Router, Routes, Route, Navigate} from "react-router-dom"
import { useState } from "react"
import LogIn from './components/LogIn'
import './App.css'
import HomePage from "./components/HomePage";

function App() {

const[isAuthenticated, setIsAuthenticated] = useState(() =>{
  return localStorage.getItem("auth") === "true"
  });
const handleAuth = (value) => {
  setIsAuthenticated(value);
  localStorage.setItem("auth", value);
}

  return (
    <Router>
      <Routes>
        {/* Login route */}
        <Route path="/login" element={<LogIn setIsAuthenticated={handleAuth} />}/>
        {/* Home route */}
        <Route
         path = "/home"
         element = {isAuthenticated ? <HomePage /> :<Navigate to ="/login" />} /> 
         {/* Default route */}
         <Route path = "*" element={<Navigate to = "/login" />} />
      </Routes>
    </Router>
  
  )
}

export default App
