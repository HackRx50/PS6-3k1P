"use client"

import React, { useEffect, useState } from 'react';

function Admin() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [uploadStatus, setUploadStatus] = useState("")

  const [taskId, setTaskId] = useState(null);


  useEffect(()=>{
    localStorage.getItem('ttvUploadTaskId') && setTaskId(localStorage.getItem('ttvUploadTaskId'))
  }, [])

  useEffect(() => {
    if (taskId) {
      const interval = setInterval(async () => {
        try {
          const statusResponse = await fetch(
            `${import.meta.env.VITE_BACKEND_URL}/check-task-status/${taskId}`
          );
          const data = await statusResponse.json();
          setUploadStatus(data.status);

          if (data.status === 'Done') {
            clearInterval(interval);
            localStorage.removeItem('ttvUploadTaskId')
          }
        } catch (error) {
          localStorage.removeItem('ttvUploadTaskId')
          console.error('Error fetching task status:', error);
        }
      }, 5000); 

      return () => clearInterval(interval); 
    }
  }, [taskId]);


  const handleFileChange = e => {
    setSelectedFile(e.target.files[0])
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadStatus("Please select a PDF file.")
      return
    }

    const formData = new FormData()
    formData.append("pdf", selectedFile)

    try {
      const response = await axios.post(import.meta.env.VITE_BACKEND_URL + "/upload_pdf", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })

      if (response.status === 200) {
        setTaskId(response.data.task_id);
        localStorage.setItem('ttvUploadTaskId', response.data.task_id)
        setUploadStatus("PDF uploaded")
      }
    } catch (error) {
      localStorage.removeItem('ttvUploadTaskId')
      setUploadStatus("Error uploading PDF. Please try again.")
    }
  };



  return (

      <div className="flex-grow flex flex-col items-center justify-center p-6">
        <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-md">
          <h2 className="text-2xl font-bold mb-4 text-center text-gray-700">Upload PDF</h2>

          <div className="mb-4">
            <input
              type="file"
              accept="application/pdf"
              onChange={handleFileChange}
              className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <button
            onClick={handleUpload}
            className="w-full px-4 py-2 bg-indigo-600 text-white rounded-md mb-4 hover:bg-indigo-700 transition duration-300"
          >
            Upload PDF
          </button>

          {uploadStatus && <p className="mt-4 text-center text-gray-600">{uploadStatus}</p>}
        </div>
      </div>
  );
}

export default Admin
