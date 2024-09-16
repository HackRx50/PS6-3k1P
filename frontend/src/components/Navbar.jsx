import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="bg-indigo-600 p-4">
      <div className="container mx-auto flex justify-between items-center">
        <div className="text-white text-lg font-semibold">My App</div>
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
            Admin
          </Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
