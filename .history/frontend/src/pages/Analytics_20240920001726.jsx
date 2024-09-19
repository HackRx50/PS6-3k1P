import React, { useEffect, useState } from 'react'
import Navbar from '../components/navbar'
import 'tailwindcss/tailwind.css'; // Ensure Tailwind CSS is imported
import { DonutChart } from '@tremor/react'; // Import DonutChart from Tremor

const Analytics = () => {
  const [data, setData] = useState(null); // State to store fetched data
  const [selectedVidName, setSelectedVidName] = useState(null); // State to track selected video

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

  const getDonutChartData = (items) => {
    return items.map(item => ({
      name: item.username,
      value: item.score,
    }));
  };

  const getFormattedData = (items) => {
    return items.map(item => ({
      name: item.username,
      amount: item.score,
    }));
  };

  return (
    <div className="min-h-screen bg-gray-100">
        <Navbar/>
        <div className="container mx-auto p-4">
          {data ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(groupByVidName(data)).map(([vidName, items]) => (
                <div 
                  key={vidName} 
                  className="bg-white shadow-md rounded-lg p-4 cursor-pointer"
                  onClick={() => setSelectedVidName(vidName)}
                >
                  <h2 className="text-xl font-bold mb-4">{vidName}</h2>
                  <DonutChart
                    data={getDonutChartData(items)}
                    width={200}
                    height={200}
                  />
                </div>
              ))}
            </div>
          ) : (
            <p className="text-center text-gray-500">Loading...</p>
          )}

          {selectedVidName && (
            <div className="mt-8">
              <h2 className="text-2xl font-bold mb-4">Analytics for {selectedVidName}</h2>
              <DonutChart
                className="mx-auto"
                data={getFormattedData(groupByVidName(data)[selectedVidName])}
                category="name"
                value="amount"
                showLabel={true}
                valueFormatter={(number) =>
                  `$${Intl.NumberFormat("us").format(number).toString()}`
                }
                width={400}
                height={400}
              />
              {groupByVidName(data)[selectedVidName].map(item => (
                <div key={item.id} className="bg-white shadow-md rounded-lg p-4 mb-4">
                  <p className="text-gray-700"><span className="font-semibold">Username:</span> {item.username}</p>
                  <p className="text-gray-700"><span className="font-semibold">Play Time:</span> {item.play_time}</p>
                  <p className="text-gray-700"><span className="font-semibold">Pause Count:</span> {item.pause_count}</p>
                  <p className="text-gray-700"><span className="font-semibold">Score:</span> {item.score}</p>
                </div>
              ))}
            </div>
          )}
        </div>
    </div>
  )
}

export default Analytics