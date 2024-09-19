import React, { useEffect, useState } from 'react'
import Navbar from '../components/navbar'

const Analytics = () => {
  const [data, setData] = useState(null); // State to store fetched data

  useEffect(() => {
    fetch('http://127.0.0.1:8000/get_all_data')
      .then(response => response.json())
      .then(data => {
        console.log(data);
        setData(data); // Store data in state
      })
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div>
        <Navbar/>
        {data ? (
          <div>
            {/* Render UI based on data */}
            <pre>{JSON.stringify(data, null, 2)}</pre>
          </div>
        ) : (
          <p>Loading...</p>
        )}
    </div>
  )
}

export default Analytics