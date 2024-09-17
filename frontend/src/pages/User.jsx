import React, { useState, useEffect, useRef } from "react"
import { useNavigate } from "react-router-dom"
import ReactPlayer from "react-player"
import Navbar from "../components/Navbar"

function App() {
  const [videos, setVideos] = useState([])
  const [selectedVideo, setSelectedVideo] = useState(null)
  const [showQuizButton, setShowQuizButton] = useState(false)
  const [pauseCount, setPauseCount] = useState(0)
  const [playTime, setPlayTime] = useState(0)
  const [lastPlayTime, setLastPlayTime] = useState(0)
  const [videoUrl, setVideoUrl] = useState(null) // State to store video URL from backend

  const playerRef = useRef(null)
  const navigate = useNavigate()

  useEffect(() => {
    // Fetch all videos from the backend
    fetch(`${import.meta.env.VITE_BACKEND_URL}/get_videos`)
      .then(response => response.json())
      .then(data => setVideos(data))
      .catch(error => console.error("Error fetching videos:", error))
  }, [])

  useEffect(() => {
    if (playerRef.current) {
      const interval = setInterval(() => {
        if (playerRef.current.getCurrentTime() > lastPlayTime) {
          setPlayTime(prevTime => prevTime + 1) // Increment play time every second
        }
      }, 1000) // Check every second if video is playing

      return () => clearInterval(interval) // Cleanup interval on component unmount
    }
  }, [lastPlayTime])

  const handleVideoEnd = () => {
    setShowQuizButton(true)
  }

  const handlePause = () => {
    setPauseCount(prevCount => prevCount + 1)
  }

  const handlePlay = () => {
    setLastPlayTime(playerRef.current.getCurrentTime())
  }

  const handleTakeQuiz = () => {
    // Passing analytics data (pause count, play time) to the quiz component
    navigate("/quiz", {
      state: { pauseCount, playTime },
    })
  }

  const handleSelectVideo = video => {
    setSelectedVideo(video)
    setShowQuizButton(false)
    setPauseCount(0)
    setPlayTime(0)
    setLastPlayTime(0)
  }
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />

      <div className="flex-grow flex flex-col items-center justify-center bg-gray-100 p-8">
        <h1 className="text-3xl font-bold mb-8">Video Library</h1>

        {selectedVideo ? (
          <div className="w-full max-w-xl bg-white shadow-lg rounded-lg overflow-hidden mb-8">
            <ReactPlayer
              ref={playerRef}
              url={`${import.meta.env.VITE_BACKEND_URL}/get_video/${selectedVideo}`}
              playing={false}
              controls
              onEnded={handleVideoEnd}
              onPause={handlePause}
              onPlay={handlePlay}
              width="100%"
              height="100%"
            />
            {showQuizButton && (
              <button
                onClick={handleTakeQuiz}
                className="w-full py-3 px-4 bg-indigo-600 text-white font-semibold hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500">
                Take Quiz
              </button>
            )}
          </div>
        ) : (
          <p className="text-xl mb-8">Select a video to watch</p>
        )}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {videos.map(video => (
            <div
              key={video}
              className="bg-white shadow-md rounded-lg overflow-hidden cursor-pointer hover:shadow-xl transition-shadow"
              onClick={() => handleSelectVideo(video)}>
              <div className="aspect-w-16 aspect-h-9 bg-gray-200">
                {/* You can add a thumbnail here if available */}
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-lg mb-2">{video}</h3>
                <p className="text-sm text-gray-600">Click to watch</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default App
