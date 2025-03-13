import {BrowserRouter as Router, Routes, Route, Navigate} from "react-router-dom"
import { useState } from "react"
import Header from "./components/Header";
import LogIn from './components/LogIn'
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
         element = {isAuthenticated ?(
          <>
          <Header setIsAuthenticated={handleAuth} />
          <HomePage setIsAuthenticated={handleAuth}  /> 
          </> 
         ):(
          <Navigate to ="/login/" />
         )} 
         />
         {/* Default route */}
         <Route path = "*" element={<Navigate to = "/login" />} />
         
      </Routes>
    </Router>
  
  )
}

export default App
