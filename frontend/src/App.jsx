import React, { useEffect } from 'react';
import Navbar from './components/Navbar';

function App() {
  // useEffect to call the FastAPI endpoint when the component is mounted
  useEffect(() => {
    const callEndpoint = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/run-tasks'); // FastAPI endpoint
        const data = await response.json();
        console.log(data.message); // Log the message from the FastAPI response
      } catch (error) {
        console.error("Error calling FastAPI endpoint:", error);
      }
    };

    callEndpoint();
  }, []); // Empty dependency array to run only once on component mount

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className='flex'>
        HACkRx
      </div>
    </div>
  );
}

export default App;
