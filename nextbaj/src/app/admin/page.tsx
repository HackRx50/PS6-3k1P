'use client'
import React, { useEffect, useState } from 'react';
import Username from '@/components/Username';
import {
  ClerkProvider,
  SignInButton,
  SignedIn,
  SignedOut,
  UserButton,
  useUser
} from '@clerk/nextjs'
import Image from 'next/image';
import { useRouter } from 'next/navigation';

function Home() {
  const { isSignedIn, isLoaded, user } = useUser();
  const [message, setMessage] = useState('');
  const router = useRouter();

  useEffect(() => {
    const createUserInBackend = async () => {
      if (isSignedIn && isLoaded && user) {
        try {
          const response = await fetch('http://localhost:8000/create_user', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              name: user.fullName,
              email: user.primaryEmailAddress?.emailAddress,
              isAdmin: false
            }),
          });
          if (!response.ok) {
            throw new Error('Failed to create user in backend');
          }
          const result = await response.json();
          console.log('User created in backend:', result);
          setMessage(result.message);
        } catch (error) {
          console.error('Error creating user in backend:', error);
          setMessage('Error creating user. Please try again.');
        }
      }
    };

    createUserInBackend();
  }, [isSignedIn, isLoaded, user]);

  const handleGetStarted = () => {
    router.push('/admin/videos');
  };

  return (
    <>
      <div className="flex-grow flex flex-col items-center justify-center p-10 text-center">
        <h1 className="text-6xl font-bold text-blue-800 mb-6 animate-fade-in-down">
          Welcome to HackrX
        </h1>
        <div className="text-2xl text-gray-600 mb-8 animate-fade-in-up">
          Empowering Innovation with Team 3k1p
        </div>
        <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full animate-fade-in">
          <h2 className="text-3xl font-semibold text-blue-700 mb-4">
            Your Journey Starts Here
          </h2>
          <button
            onClick={handleGetStarted}
            className="mt-4 px-6 py-3 bg-blue-600 text-white font-semibold rounded-full hover:bg-blue-700 transition duration-300 ease-in-out transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
          >
            Get Started
          </button>
          <p className="mt-6 text-gray-600">
            Join us in shaping the future of technology and creativity.
          </p>
        </div>
      </div>
      <footer className="bg-blue-800 text-white py-4 text-center">
        <p>&copy; 2024 HackrX. All rights reserved.</p>
      </footer>
    </>
  );
}

export default Home;