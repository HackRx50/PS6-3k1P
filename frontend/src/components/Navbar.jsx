import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="bg-blue-800 p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <Link
          to="/"
          className="text-white text-lg font-semibold hover:text-blue-200 transition">Home</Link>
        <div className="space-x-4">
          <Link
            to="/user"
            className="text-white hover:bg-blue-700 hover:text-blue-100 py-2 px-4 rounded transition"
          >
            User
          </Link>
          <Link
            to="/admin"
            className="text-white hover:bg-blue-700 hover:text-blue-100 py-2 px-4 rounded transition"
          >
            Generate Video
          </Link>
          <Link
            to="/analytics"
            className="text-white hover:bg-blue-700 hover:text-blue-100 py-2 px-4 rounded transition"
          >
            Admin Analytics
          </Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;