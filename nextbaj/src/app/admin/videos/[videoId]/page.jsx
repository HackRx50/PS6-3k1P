"use client";

import React, { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import ReactPlayer from "react-player";

const Page = () => {
  const [videoData, setVideoData] = useState(null);
  const [selectedLanguage, setSelectedLanguage] = useState(null);
  const [playing, setPlaying] = useState(false);
  const { videoId } = useParams();
  const router = useRouter();

  useEffect(() => {
    const fetchVideoData = async () => {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/get_video_id/${videoId}`
        );
        if (!response.ok) {
          throw new Error("Failed to fetch video data");
        }
        const data = await response.json();
        setVideoData(data);
        setSelectedLanguage(data.languages.split(",")[0]); // Set default to first language
      } catch (error) {
        console.error("Error fetching video data:", error);
      }
    };

    fetchVideoData();
  }, [videoId]);

  if (!videoData) {
    return (
      <div className="flex justify-center items-center h-screen bg-gray-100">
        <div className="animate-spin rounded-full h-32 w-32 border-t-4 border-b-4 border-blue-500"></div>
      </div>
    );
  }

  const languages = videoData.languages.split(",");

  const handleLanguageChange = (event) => {
    setSelectedLanguage(event.target.value);
    setPlaying(true);
  };

  const handleBack = () => {
    router.push("/admin/videos");
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-blue-200 flex flex-col items-center p-8">
      <button
        onClick={handleBack}
        className="absolute top-4 left-4 py-2 px-6 bg-blue-600 text-white font-bold rounded-md shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-300"
      >
        Back to Videos
      </button>

      <h1 className="text-5xl font-extrabold text-blue-900 mb-8 text-center">
        {videoData.name}
      </h1>

      {/* Primary View: Video Player */}
      <div className="w-full max-w-5xl bg-white shadow-2xl rounded-lg overflow-hidden mb-8">
        <div className="p-6">
          <div className="mb-4">
            {/* Dropdown for selecting language */}
            <label className="block mb-2 text-lg font-medium text-gray-700">
              Select Language:
            </label>
            <select
              value={selectedLanguage}
              onChange={handleLanguageChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {languages.map((language, index) => (
                <option key={index} value={language}>
                  {language}
                </option>
              ))}
            </select>
          </div>

          <div style={{ width: '100%', height: '600px' }}>
      <ReactPlayer
        url={videoData.youtube_url}
        playing={playing}
        controls={true}
        width="100%"
        height="100%"
        className="rounded-lg"
      />
    </div>
        </div>
      </div>

      {/* Secondary View: Video Description and Details */}
      <div className="w-full max-w-4xl bg-white shadow-2xl rounded-lg overflow-hidden">
        <div className="p-6">
          <h2 className="text-2xl font-bold text-blue-800 mb-4">Video Details</h2>
          <p className="text-lg text-gray-800 mb-4">
            <span className="font-bold">Description:</span> {videoData.description}
          </p>
          <p className="text-md text-gray-700 mb-2">
            <span className="font-semibold">Duration:</span> {videoData.duration} minutes
          </p>
          <p className="text-md text-gray-700">
            <span className="font-semibold">Number of Slides:</span> {videoData.no_slides}
          </p>
        </div>
      </div>
    </div>
  );
};

export default Page;
