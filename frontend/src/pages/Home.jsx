import React from 'react';
import Navbar from '../components/Navbar';
import Username from '../components/Username';

function Home() {
  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-r from-blue-50 to-blue-100">
      <Navbar />
      <div className='p-10'>
        HackrX
        <div>
          Team 3k1p
        </div>
        <Username />
      </div>
    </div>
  );
}

export default Home;
