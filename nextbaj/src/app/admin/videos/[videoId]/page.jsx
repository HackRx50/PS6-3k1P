"use client"

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import ReactPlayer from 'react-player';
import Image from 'next/image';

const Page = () => {
  const [videoData, setVideoData] = useState(null);
  const [selectedLanguage, setSelectedLanguage] = useState(null);
  const [playing, setPlaying] = useState(false);
  const { videoId } = useParams();
  const router = useRouter();

  useEffect(() => {
    const fetchVideoData = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/get_video_id/${videoId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch video data');
        }
        const data = await response.json();
        setVideoData(data);
      } catch (error) {
        console.error('Error fetching video data:', error);
      }
    };

    
    fetchVideoData();
  }, [videoId]);

  if (!videoData) {
    return <div className="flex justify-center items-center h-screen">
      <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-500"></div>
    </div>;
  }

  const languages = videoData.languages.split(',');

  const handleCardClick = (language) => {
    setSelectedLanguage(language);
    setPlaying(true);
  };

  const handleBack = () => {
    router.push('/admin/videos');
  };

  return (
    <div className="flex-grow flex flex-col items-center justify-center p-8">
      <button
        onClick={handleBack}
        className="absolute top-4 left-4 py-2 px-4 bg-blue-600 text-white font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-300"
      >
        Back to Videos
      </button>
      
      <h1 className="text-4xl font-extrabold text-blue-800 mb-8">{videoData.name}</h1>
      
      <div className="w-full max-w-4xl bg-white shadow-2xl rounded-lg overflow-hidden mb-8">
        <div className="p-6">
          <p className="text-lg text-gray-700 mb-4">Description: {videoData.description}</p>
          <p className="text-md text-gray-600">Duration: {videoData.duration} minutes</p>
          <p className="text-md text-gray-600">Number of Slides: {videoData.no_slides}</p>
        </div>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 mb-8">
        {languages.map((language, index) => (
          <div
            key={index}
            className="bg-white shadow-lg rounded-lg overflow-hidden cursor-pointer hover:shadow-2xl transition-shadow duration-300 flex flex-col"
            onClick={() => handleCardClick(language)}
            style={{ width: '200px', height: '100px' }}
          >
            <div className="p-4 flex-grow flex items-center justify-center">
              <h3 className="font-semibold text-lg text-blue-800">{language}</h3>
            </div>
          </div>
        ))}
      </div>

      {selectedLanguage && (
        <div className="w-full max-w-4xl bg-white shadow-2xl rounded-lg overflow-hidden">
          <div className="p-6">
            <h2 className="text-2xl font-bold text-blue-800 mb-4">Playing video in {selectedLanguage}</h2>
            <div className="aspect-w-16 aspect-h-9">
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
      )}
    </div>
  );
};

export default Page;