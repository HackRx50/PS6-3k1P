"use client";

import { useUser } from '@clerk/nextjs';
import React, { useState } from 'react';

const Username = () => {
  const { user } = useUser();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newName, setNewName] = useState('');

  const handleEdit = () => {
    setIsModalOpen(true);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Updated name:', newName);
    setIsModalOpen(false);
    setNewName('');
  };

  return (
    <div className='text-white'>
      <span>{user?.fullName || 'Anonymous User'}</span>
      <button onClick={handleEdit} aria-label="Edit name" className="ml-2 text-blue-400 hover:text-blue-300">
        ✏️
      </button>
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-gray-800 p-8 rounded-xl shadow-2xl max-w-md w-full">
            <h2 className="text-2xl font-semibold mb-6 text-white">Edit Name</h2>
            <form onSubmit={handleSubmit}>
              <input
                type="text"
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
                placeholder="Enter new name"
                className="bg-gray-700 text-white border border-gray-600 p-3 rounded-lg mb-6 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <div className="flex justify-end space-x-4">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 text-gray-300 hover:text-white transition-colors duration-200"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors duration-200"
                >
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Username;