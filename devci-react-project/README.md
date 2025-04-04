# React + Vite
React-Flask User Registration System
This project is a pharmacy verification system that integrates a React frontend with a Flask backend, allowing pharmacists to verify a prescription is actually from a doctor with different roles such as doctor, pharmacist, and admin. The system handles role-specific information and stores user data securely

Project Overview
This application provides a seamless interface for prescription verification, catering to different roles with specific attributes. The React frontend offers an intuitive form for data entry, while the Flask backend manages data processing and storage.

Features
Role-Based Registration: Supports registration for doctors, pharmacists, and admins, each with unique fields.

Secure Password Handling: Utilizes hashing to store passwords securely.

API Integration: Communicates between frontend and backend using RESTful APIs.

Database Storage: Stores user information in a SQLite database.

Technologies Used
Frontend: React, HTML, CSS, JavaScript

Backend: Flask, Python

Database: SQLite

Other Tools: Node.js, npm, Create React App

Getting Started
Follow these instructions to set up and run the project on your local machine.

Prerequisites
Ensure you have the following installed:

Node.js and npm

Python 3

Installation
Clone the Repository:
git clone https://github.com/Ursullah/devci-react-project.git
cd react-flask-registration

Set Up the Backend:
Navigate to the backend directory:
cd backend

Create a virtual environment:
python3 -m venv venv
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'

Install required Python packages:
pip install flask flask-cors werkzeug

Set up the SQLite database:
flask init-db

Set Up the Frontend:
cd devci-react-project
Install npm packages:
npm install

Running the Application
Start the Backend Server:

In the backend directory, activate the virtual environment if not already active:
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'

Run the Flask application:
python app.py
The backend server will start on http://localhost:5000.

Start the Frontend Server:

In a new terminal, navigate to the frontend directory:

cd frontend
Start the React development server:
npm run dev
The frontend will be running on http://localhost:5173.

Usage
Accessing the Application:

Open your browser and navigate to http://localhost:5173 to access the registration form.

Registering a User:

Fill in the required fields in the registration form.

Select the appropriate role to reveal role-specific fields.

Submit the form to register the user.

Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.

Create a new branch (git checkout -b feature/your-feature).

Commit your changes (git commit -m 'Add some feature').

Push to the branch (git push origin feature/your-feature).

Open a pull request.