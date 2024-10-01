"use client";

import React, { useState, useEffect } from 'react';

const generateRandomUsername = () => {
  const adjectives = ["happy", "lucky", "sunny", "clever", "swift"];
  const nouns = ["cat", "dog", "bird", "fish", "fox"];
  return `${adjectives[Math.floor(Math.random() * adjectives.length)]}${nouns[Math.floor(Math.random() * nouns.length)]}`;
};

const Username = () => {
  const [username, setUsername] = useState('');

  useEffect(() => {
    const storedUsername = localStorage.getItem('username');
    if (storedUsername) {
      setUsername(storedUsername);
    } else {
      const newUsername = generateRandomUsername();
      setUsername(newUsername);
      localStorage.setItem('username', newUsername);
    }
  }, []);

  const handleEdit = () => {
    const newUsername = prompt("Enter new username:", username);
    if (newUsername) {
      setUsername(newUsername);
      localStorage.setItem('username', newUsername);
    }
  };

  return (
    <div>
      <span>{username}</span>
      <button onClick={handleEdit} aria-label="Edit username">
        ✏️
      </button>
    </div>
  );
};

export default Username;