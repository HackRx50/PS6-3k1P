import React, { useEffect } from 'react'
import Navbar from '../components/navbar'

const Analytics = () => {
  useEffect(() => {
    fetch('http://127.0.0.1:8000/get_all_data')
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div>
        <Navbar>
    </div>
  )
}

export default Analytics