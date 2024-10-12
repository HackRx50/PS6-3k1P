"use client";

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation'; // Import useRouter
import ReactPlayer from 'react-player';

const VideoPage = () => {
  const router = useRouter();
  const searchParams = new URLSearchParams(window.location.search);
  const id = searchParams.get('id'); // Extract the id from the search params
  
  const [videoData, setVideoData] = useState(null);
  const [playing, setPlaying] = useState(false);

  useEffect(() => {
    if (!id) return; // Wait for the id to be available

    const fetchVideo = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/get_video_id/${id}`);
        if (!response.ok) {
          throw new Error('Failed to fetch video');
        }
        const data = await response.json();
        console.log(data);
        setVideoData(data);
      } catch (error) {
        console.error('Error fetching video:', error);
      }
    };

    fetchVideo();
  }, [id]);

  if (!videoData) {
    return <div>Loading...</div>; // Show a loading state until the video data is fetched
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8">
      <h1 className="text-4xl font-extrabold text-blue-800 mb-8">{videoData.name}</h1>
      <div className="w-full max-w-4xl">
  <div className="relative" style={{ paddingTop: '56.25%' }}> {/* 16:9 aspect ratio */}
    <ReactPlayer
      url={videoData.youtube_url}
      playing={playing}
      controls={true}
      width="100%"
      height="100%"
      style={{ position: 'absolute', top: 0, left: 0 }} 
      onPlay={() => setPlaying(true)}
      onPause={() => setPlaying(false)}
    />
  </div>
</div>

    </div>
  );
};

export default VideoPage;
