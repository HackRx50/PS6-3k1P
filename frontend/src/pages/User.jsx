import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import ReactPlayer from "react-player";
import Navbar from "../components/Navbar";

function User() {
  const [videos, setVideos] = useState([]);
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [showQuizButton, setShowQuizButton] = useState(false);
  const [pauseCount, setPauseCount] = useState(0);
  const [playTime, setPlayTime] = useState(0);
  const [playing, setPlaying] = useState(false);

  const playerRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`${import.meta.env.VITE_BACKEND_URL}/get_videos`)
      .then((response) => response.json())
      .then((data) => setVideos(data))
      .catch((error) => console.error("Error fetching videos:", error));
  }, []);

  const handleVideoEnd = () => {
    setShowQuizButton(true);
    setPlaying(false);
  };

  const handlePause = () => {
    setPauseCount((prevCount) => prevCount + 1);
    setPlaying(false);
  };

  const handlePlay = () => {
    setShowQuizButton(false);
    setPlaying(true);
  };

  const handleProgress = (state) => {
    setPlayTime(state.playedSeconds);
  };

  const handleSeek = (seconds) => {
    setPlayTime(seconds);
    setPlaying(true);
  };

  const handleTakeQuiz = () => {
    navigate("/quiz", {
      state: { selectedVideo, pauseCount, playTime },
    });
  };

  const handleSelectVideo = (video) => {
    setSelectedVideo(video);
    setShowQuizButton(false);
    setPauseCount(0);
    setPlayTime(0);
    setPlaying(false);
  };

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-r from-blue-50 to-blue-100">
      <Navbar />
      <div className="flex-grow flex flex-col items-center justify-center p-8">
        <h1 className="text-4xl font-extrabold text-blue-800 mb-8">Video Library</h1>

        {selectedVideo ? (
          <div className="w-full max-w-2xl bg-white shadow-2xl rounded-lg overflow-hidden mb-8">
            <ReactPlayer
              ref={playerRef}
              url={`${import.meta.env.VITE_BACKEND_URL}/get_video/${selectedVideo}`}
              playing={playing}
              controls={true}
              onEnded={handleVideoEnd}
              onPause={handlePause}
              onPlay={handlePlay}
              onProgress={handleProgress}
              onSeek={handleSeek}
              width="100%"
              height="100%"
              className="rounded-t-lg"
            />
            {showQuizButton && (
              <button
                onClick={handleTakeQuiz}
                className="w-full py-3 px-4 bg-blue-600 text-white font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-300"
              >
                Take Quiz
              </button>
            )}
          </div>
        ) : (
          <p className="text-2xl text-blue-700 mb-8">Select a video to watch</p>
        )}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
          {videos.map((video) => (
            <div
              key={video}
              className="bg-white shadow-lg rounded-lg overflow-hidden cursor-pointer hover:shadow-2xl transition-shadow duration-300"
              onClick={() => handleSelectVideo(video)}
            >
              <div className="aspect-w-16 aspect-h-9 bg-gray-200">
                {/* <img
                  src={`${import.meta.env.VITE_BACKEND_URL}/get_thumbnail/${video}`}
                  alt={`${video} thumbnail`}
                  className="w-full h-full object-cover"
                /> */}
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-xl text-blue-800 mb-2">{video}</h3>
                <p className="text-sm text-gray-600">Click to watch</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default User;