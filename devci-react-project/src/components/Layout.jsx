import { Outlet, Link } from "react-router-dom";

const Layout = () => {
  return (
    <div>
      {/* 🔹 Persistent Header */}
      <header className="bg-slate-800 text-white py-4 px-6 flex justify-between items-center">
        <h1 className="text-xl font-bold">DEVCI</h1>
        <nav>
          <ul className="flex space-x-4">
            <li><Link to="/" className="hover:underline">Home</Link></li>
            <li><Link to="/about" className="hover:underline">About</Link></li>
            <li><Link to="/contact" className="hover:underline">Contact</Link></li>
          </ul>
        </nav>
      </header>

      {/* 🔹 This will change based on the route */}
      <main>
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
