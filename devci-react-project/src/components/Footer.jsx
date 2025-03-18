import React from 'react'

const Footer = () => {
  return (
    <div>
         {/* Footer */}
         <footer className="w-full py-4 bg-gray-800 text-center text-sm text-gray-400">
        &copy; {new Date().getFullYear()} Prescription Verifier. All rights reserved.
      </footer>
    </div>
  )
}

export default Footer
