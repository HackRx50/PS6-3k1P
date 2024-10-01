import React from 'react';
import Username from '@/components/Username';

function Home() {
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
          <div className="flex items-center justify-center p-4 bg-blue-50 rounded-lg border-2 border-blue-300 shadow-inner">
            <span className="mr-2 text-blue-700 font-semibold">Username:</span>
            <div className="bg-white px-3 py-2 rounded-md shadow-sm">
              <Username />
            </div>
          </div>
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