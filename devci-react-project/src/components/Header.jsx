import React from 'react'

const Header = () => {
  return (
    <div>
      <nav>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/services">Services</Link></li>
        <li><Link to="/about">About</Link></li>
        <li><Link to="/contact">Contact</Link></li>
      </ul>
    </nav>
    </div>
  )
}

export default Header
