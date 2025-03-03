"use client";

import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import ReactPlayer from "react-player";
import Image from "next/image";

function User() {
  const [videos, setVideos] = useState([]);
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [showQuizButton, setShowQuizButton] = useState(true);
  const [pauseCount, setPauseCount] = useState(0);
  const [playTime, setPlayTime] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [youtubeLinks, setYoutubeLinks] = useState({});
  const [selectedPlatform, setSelectedPlatform] = useState(null);

  const playerRef = useRef(null);
  const videoPlayerRef = useRef(null);

  const router = useRouter();

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/get_files`)
      .then((response) => response.json())
      .then((data) => {
        console.log("Fetched data:", data);
        setVideos(data);
        const storedLinks = JSON.parse(
          localStorage.getItem("youtubeLinks") || "{}"
        );
        setYoutubeLinks(storedLinks);
      })
      .catch((error) => console.error("Error fetching videos:", error));
  }, []);

  const handleVideoEnd = () => {
    setPlaying(false);
  };

  const handlePause = () => {
    setPauseCount((prevCount) => prevCount + 1);
    setPlaying(false);
  };

  const handlePlay = () => {
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
    const videoName = selectedVideo;

    const quizUrl = `/quiz?video_name=${encodeURIComponent(videoName)}`;

    router.push(quizUrl);
  };

  const handleSelectVideo = (video) => {
    setSelectedVideo(video);
    setPauseCount(0);
    setPlayTime(0);
    setPlaying(false);
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  const handleExport = () => {
    setIsModalOpen(true);
    setSelectedPlatform("youtube");
  };

  const handlePublish = async () => {
    if (!selectedVideo) return;

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/publish_to_youtube`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            file: selectedVideo,
            title: selectedVideo,
            description: "Uploaded from my app",
            keywords: "video,upload",
            category: "22",
            privacyStatus: "public",
          }),
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Error response:", response.status, errorText);
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      const youtubeLink = `https://www.youtube.com/watch?v=${result.video_id}`;
      setYoutubeLinks((prevLinks) => {
        const newLinks = { ...prevLinks, [selectedVideo]: youtubeLink };
        localStorage.setItem("youtubeLinks", JSON.stringify(newLinks));
        return newLinks;
      });

      alert(`Video published successfully to YouTube!`);
      console.log("Publish result:", result);
    } catch (error) {
      console.error("Error publishing video:", error);
      alert("An error occurred while publishing the video: " + error.message);
    }

    setIsModalOpen(false);
  };

  return (
    <div className="flex-grow flex flex-col items-center justify-center p-8">
      {selectedVideo ? (
        <div
          ref={videoPlayerRef}
          className="w-full max-w-4xl bg-white shadow-2xl rounded-lg overflow-hidden mb-8"
        >
          <div className="aspect-w-16 aspect-h-9">
            <ReactPlayer
              ref={playerRef}
              url={`${process.env.NEXT_PUBLIC_API_URL}/get_file/${selectedVideo}`}
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
          </div>
          <div className="p-6">
            <h2 className="text-2xl font-bold text-blue-800 mb-4 truncate">
              {selectedVideo}
            </h2>
            {youtubeLinks[selectedVideo] && (
              <div className="mb-4">
                <p className="text-sm text-gray-600 mb-1">YouTube Link:</p>
                <a
                  href={youtubeLinks[selectedVideo]}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline truncate block"
                >
                  {youtubeLinks[selectedVideo]}
                </a>
              </div>
            )}
            <div className="flex justify-between">
              {showQuizButton && (
                <button
                  onClick={handleTakeQuiz}
                  className="w-1/2 py-3 px-4 bg-blue-600 text-white font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-300 mr-2"
                >
                  Take Quiz
                </button>
              )}
              <button
                onClick={handleExport}
                className="w-1/2 py-3 px-4 bg-green-600 text-white font-semibold hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 transition duration-300 ml-2"
              >
                Export
              </button>
            </div>
          </div>
        </div>
      ) : (
        <p className="text-2xl text-blue-700 mb-8">Select a video to watch</p>
      )}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
        {Array.isArray(videos) ? (
          videos.map((video) => (
            <div
              key={video}
              className="bg-white shadow-lg rounded-lg overflow-hidden cursor-pointer hover:shadow-2xl transition-shadow duration-300 flex flex-col"
              onClick={() => handleSelectVideo(video)}
              style={{ width: "300px", height: "300px" }}
            >
              <div className="p-4 flex-grow flex flex-col">
                <h3 className="font-semibold text-lg text-blue-800 truncate">
                  {video}
                </h3>
                {youtubeLinks[video] && (
                  <a
                    href={youtubeLinks[video]}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-blue-600 hover:underline truncate mt-1"
                  >
                    YouTube Link
                  </a>
                )}
              </div>
            </div>
          ))
        ) : (
          <p>Loading videos...</p>
        )}
      </div>

      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white p-8 rounded-lg">
            <h2 className="text-2xl font-bold mb-4">Publish to YouTube</h2>
            <p className="mb-4">
              Are you sure you want to publish "{selectedVideo}" to YouTube?
            </p>
            <div className="flex justify-end">
              <button
                onClick={() => setIsModalOpen(false)}
                className="mr-2 px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400"
              >
                Cancel
              </button>
              <button
                onClick={handlePublish}
                className="px-4 py-2 text-white rounded bg-blue-600 hover:bg-blue-700"
              >
                Publish
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default User;
