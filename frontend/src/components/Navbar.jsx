import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="bg-indigo-600 p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link
          to="/"
          className="text-white text-lg font-semibold">My App</Link>
        <div className="space-x-4">
          <Link
            to="/user"
            className="text-white hover:bg-indigo-700 py-2 px-4 rounded transition"
          >
            User
          </Link>
          <Link
            to="/admin"
            className="text-white hover:bg-indigo-700 py-2 px-4 rounded transition"
          >
            Admin Upload
          </Link>
          <Link
            to="/analytics"
            className="text-white hover:bg-indigo-700 py-2 px-4 rounded transition"
          >
            Admin Analytics
          </Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
