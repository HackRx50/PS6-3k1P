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

function Home() {
  const { isSignedIn, isLoaded, user } = useUser();
  const [message, setMessage] = useState('');

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

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-400 to-blue-500 text-white">
      <main className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-6xl font-extrabold mb-6">
            Welcome to <span className="text-yellow-300">Avocado AI</span>
          </h1>
          <p className="text-2xl mb-8 max-w-3xl mx-auto">
            Revolutionize Your Content Creation with AI-Powered Video Generation
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
          <div className="bg-white bg-opacity-20 rounded-lg p-6">
            <h2 className="text-4xl font-bold mb-6">Transform Your Ideas</h2>
            <ul className="space-y-4 text-xl">
              <li>🚀 Convert documents to engaging videos</li>
              <li>🌍 Generate multilingual content effortlessly</li>
              <li>📈 Boost your YouTube channel with AI creativity</li>
              <li>⏱️ Save time and resources in content production</li>
            </ul>
          </div>
          <div className="flex justify-center">
            <Image
              src="/avocado-ai-logo.jpeg"
              alt="Avocado AI Logo"
              width={400}
              height={400}
              className="rounded-full shadow-2xl animate-pulse"
            />
          </div>
        </div>

        <div className="mt-16 text-center">
          <h2 className="text-3xl font-bold mb-6">Ready to Get Started?</h2>
          <div className="inline-block bg-white bg-opacity-20 rounded-lg p-4">
            <span className="mr-2 text-yellow-300 font-semibold">Your Username:</span>
            <div className="inline-block bg-white bg-opacity-10 px-3 py-2 rounded-md">
              <Username />
            </div>
          </div>
        </div>
      </main>
      <footer className="bg-white bg-opacity-10 text-white py-4 text-center mt-16">
        <p>&copy; 2024 Avocado AI. Empowering content creators worldwide.</p>
      </footer>
    </div>
  );
}

export default Home;