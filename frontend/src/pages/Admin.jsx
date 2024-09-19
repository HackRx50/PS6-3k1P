import React, { useState } from 'react';
import axios from 'axios';


function Admin() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [uploadStatus, setUploadStatus] = useState("")

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
        setUploadStatus("PDF uploaded successfully!")
      }
    } catch (error) {
      setUploadStatus("Error uploading PDF. Please try again.")
    }
  };

  const navigateToAnalytics = () => {
    window.location.href = '/analytics';
  };

  const navigateToHome = () => {
    window.location.href = '/';
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <nav className="bg-blue-600 p-4 shadow-md">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-white text-2xl font-bold">Admin Dashboard</h1>
          <div>
            <button
              onClick={navigateToHome}
              className="px-4 py-2 bg-green-500 text-white rounded-md mr-2 hover:bg-gray-600 transition duration-300"
            >
              Home
            </button>
            <button
              onClick={navigateToAnalytics}
              className="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 transition duration-300"
            >
              Go to Analytics
            </button>
          </div>
        </div>
      </nav>

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
    </div>
  );
}

export default Admin
