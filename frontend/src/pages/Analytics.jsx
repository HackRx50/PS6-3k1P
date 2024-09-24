import React, { useEffect, useState } from "react"
import Navbar from "../components/Navbar"
import "tailwindcss/tailwind.css" // Ensure Tailwind CSS is imported
import { BarChart } from "../components/BarChart"
import { DonutChart } from "../components/DonutChart"

const Analytics = () => {
  const [data, setData] = useState(null) // State to store fetched data
  const [selectedVidName, setSelectedVidName] = useState(null) // State to track selected video

  useEffect(() => {
    fetch(`${import.meta.env.VITE_BACKEND_URL}/get_all_data`)
      .then(response => response.json())
      .then(data => {
        console.log(data)
        setData(data)
      })
      .catch(error => console.error("Error fetching data:", error))
  }, [])

  const groupByVidName = data => {
    return data.reduce((acc, item) => {
      if (!acc[item.vid_name]) {
        acc[item.vid_name] = []
      }
      acc[item.vid_name].push(item)
      return acc
    }, {})
  }

  const allData = data
    ? Object.entries(groupByVidName(data)).map(([vidName, items]) => {
        const total = items.reduce(
          (acc, item) => {
            acc.score += item.score
            acc.pause_count += item.pause_count
            acc.play_time += item.play_time
            return acc
          },
          { score: 0, pause_count: 0, play_time: 0 }
        )

        return {
          vidName,
          averageScore: total.score / items.length,
          averagePauseCount: total.pause_count / items.length,
          averagePlayTime: total.play_time / items.length,
        }
      })
    : []

  console.log("dd", allData)

  const curData = data && selectedVidName ? groupByVidName(data)[selectedVidName] : []

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      <div className="container mx-auto p-4">
        {data ? (
          <div>
            <div className="mb-4 flex flex-row gap-5">
              <div className="p-4 w-96 bg-white shadow-md rounded-lg overflow-hidden cursor-pointer">
                <p className="text-center text-3xl font-bold text-gray-700 mb-3">Total</p>
                <p className="text-center text-lg text-gray-700 ">
                  Total Users: {data.length} {/* Assuming each item in data represents a user */}
                </p>
                <p className="text-center text-lg text-gray-700">
                  Videos Viewed: {allData.length} {/* Total number of unique videos */}
                </p>
              </div>
              <div className="p-4 w-96 bg-white shadow-md rounded-lg overflow-hidden cursor-pointer">
                <p className="text-center text-lg font-semibold text-gray-700 ">Average Score</p>
                <DonutChart
                  variant="pie"
                  className="ml-10 h-60"
                  data={allData}
                  category="vidName"
                  value="averageScore"
                  valueFormatter={number => `${Intl.NumberFormat("us").format(number).toString()}`}
                  onValueChange={v => console.log(v)}
                />
              </div>

              <div className="p-4 w-96 bg-white shadow-md rounded-lg overflow-hidden cursor-pointer">
                <p className="text-center text-lg font-semibold text-gray-700 ">Average Pauses</p>
                <DonutChart
                  variant="pie"
                  className="ml-10 h-60"
                  data={allData}
                  category="vidName"
                  value="averagePauseCount"
                  valueFormatter={number => `${Intl.NumberFormat("us").format(number).toString()}`}
                  onValueChange={v => console.log(v)}
                />
              </div>

              <div className="p-4 w-96 bg-white shadow-md rounded-lg overflow-hidden cursor-pointer">
                <p className="text-center text-lg font-semibold text-gray-700 ">Average Play Time</p>
                <DonutChart
                  variant="pie"
                  className="ml-10 h-60"
                  data={allData}
                  category="vidName"
                  value="averagePlayTime"
                  valueFormatter={number => `${Intl.NumberFormat("us").format(number).toString()}s`}
                  onValueChange={v => console.log(v)}
                />
              </div>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
              {Object.entries(groupByVidName(data)).map(([vidName, items]) => (
                <div
                  key={vidName}
                  className="w-80 bg-white shadow-md rounded-lg p-4 cursor-pointer"
                  onClick={() => setSelectedVidName(vidName)}>
                  <h2 className="text-xl font-bold mb-4">{vidName}</h2>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <p className="text-center text-gray-500">Loading...</p>
        )}

        {selectedVidName && (
          <div className="mt-8">
            <h2 className="text-2xl font-bold mb-4">Analytics for {selectedVidName}</h2>

            <div className="grid grid-cols-3 gap-5">
              <div className="p-4 bg-white shadow-md rounded-lg overflow-hidden cursor-pointer">
                <BarChart
                  className="h-80"
                  data={curData}
                  colors={["blue"]}
                  index="username"
                  categories={["score"]}
                  valueFormatter={number => `${Intl.NumberFormat("us").format(number).toString()}`}
                  onValueChange={v => console.log(v)}
                />
              </div>

              <div className="p-4 bg-white shadow-md rounded-lg overflow-hidden cursor-pointer">
                <BarChart
                  className="h-80"
                  data={curData}
                  colors={["emerald"]}
                  index="username"
                  categories={["pause_count"]}
                  valueFormatter={number => `${Intl.NumberFormat("us").format(number).toString()}`}
                  onValueChange={v => console.log(v)}
                />
              </div>

              <div className="p-4 bg-white shadow-md rounded-lg overflow-hidden cursor-pointer">
                <BarChart
                  className="h-80"
                  data={curData}
                  colors={["violet"]}
                  index="username"
                  categories={["play_time"]}
                  valueFormatter={number => `${Intl.NumberFormat("us").format(number).toString()}s`}
                  onValueChange={v => console.log(v)}
                />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Analytics
