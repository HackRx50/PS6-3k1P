import React, { useState } from "react"
import axios from "axios"
import Navbar from "../components/Navbar"

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
  }

  return (
    <>
      <Navbar />

      <div className="flex justify-center items-center ">
        <div className="mt-10 border-2 border-gray-300 border-dashed rounded-lg p-6 bg-white">
          <h1 className="text-2xl font-bold mb-4">Upload PDF</h1>

          <div className="mb-4">
            <input type="file" accept="application/pdf" onChange={handleFileChange} />
          </div>

          <button onClick={handleUpload} className="px-4 py-2 bg-indigo-600 text-white rounded-md">
            Upload PDF
          </button>

          {uploadStatus && <p className="mt-4">{uploadStatus}</p>}
        </div>
      </div>
    </>
  )
}

export default Admin
