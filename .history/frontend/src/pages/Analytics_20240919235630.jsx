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

  const groupByVidName = (data) => {
    return data.reduce((acc, item) => {
      if (!acc[item.vid_name]) {
        acc[item.vid_name] = [];
      }
      acc[item.vid_name].push(item);
      return acc;
    }, {});
  };

  return (
    <div>
        <Navbar/>
        {data ? (
          <div>
            {Object.entries(groupByVidName(data)).map(([vidName, items]) => (
              <div key={vidName} className="card">
                <h2>{vidName}</h2>
                {items.map(item => (
                  <div key={item.id} className="card-item">
                    <p>Username: {item.username}</p>
                    <p>Play Time: {item.play_time}</p>
                    <p>Pause Count: {item.pause_count}</p>
                    <p>Score: {item.score}</p>
                  </div>
                ))}
              </div>
            ))}
          </div>
        ) : (
          <p>Loading...</p>
        )}
    </div>
  )
}

export default Analytics