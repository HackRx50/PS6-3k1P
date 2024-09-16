import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import ReactPlayer from 'react-player';

function App() {
  const [showQuizButton, setShowQuizButton] = useState(false);
  const [pauseCount, setPauseCount] = useState(0);
  const [playTime, setPlayTime] = useState(0);
  const [lastPlayTime, setLastPlayTime] = useState(0);
  const [videoUrl, setVideoUrl] = useState(null);  // State to store video URL from backend

  const playerRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch the video from the backend
    fetch(import.meta.env.VITE_BACKEND_URL+'/get_video/sample.mp4')
      .then((response) => response.url)
      .then((url) => setVideoUrl(url))
      .catch((error) => console.error('Error fetching video:', error));
  }, []);

  useEffect(() => {
    if (playerRef.current) {
      const interval = setInterval(() => {
        if (playerRef.current.getCurrentTime() > lastPlayTime) {
          setPlayTime((prevTime) => prevTime + 1); // Increment play time every second
        }
      }, 1000); // Check every second if video is playing

      return () => clearInterval(interval); // Cleanup interval on component unmount
    }
  }, [lastPlayTime]);

  const handleVideoEnd = () => {
    setShowQuizButton(true);
  };

  const handlePause = () => {
    setPauseCount((prevCount) => prevCount + 1);
  };

  const handlePlay = () => {
    setLastPlayTime(playerRef.current.getCurrentTime());
  };

  const handleTakeQuiz = () => {
    // Passing analytics data (pause count, play time) to the quiz component
    navigate('/quiz', {
      state: { pauseCount, playTime }
    });
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <div className="w-full max-w-xl p-8 bg-white shadow-lg rounded-lg">
        <h1 className="text-2xl font-bold mb-4">Watch the Video</h1>

        {/* ReactPlayer to track play time and pauses */}
        {videoUrl ? (
          <ReactPlayer
            ref={playerRef}
            url={videoUrl}
            playing={false}
            controls
            onEnded={handleVideoEnd}
            onPause={handlePause}
            onPlay={handlePlay}
            width="100%"
            height="100%"
          />
        ) : (
          <p>Loading video...</p>
        )}

        {/* Show quiz button after video ends */}
        {showQuizButton && (
          <button
            onClick={handleTakeQuiz}
            className="w-full py-3 px-4 bg-indigo-600 text-white font-semibold rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            Take Quiz
          </button>
        )}
      </div>
    </div>
  );
}

export default App;
