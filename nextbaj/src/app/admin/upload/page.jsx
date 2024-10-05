"use client"

import { useEffect, useState } from "react"

function Admin() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [uploadStatus, setUploadStatus] = useState("")

  const [taskId, setTaskId] = useState(null)

  useEffect(() => {
    localStorage.getItem("ttvUploadTaskId") && setTaskId(localStorage.getItem("ttvUploadTaskId"))
  }, [])

  useEffect(() => {
    if (taskId) {
      const interval = setInterval(async () => {
        try {
          const statusResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/check-task-status/${taskId}`)
          const data = await statusResponse.json()
          setUploadStatus(data.status)

          if (data.status === "Done") {
            clearInterval(interval)
            localStorage.removeItem("ttvUploadTaskId")
          }
        } catch (error) {
          localStorage.removeItem("ttvUploadTaskId")
          console.error("Error fetching task status:", error)
        }
      }, 5000)

      return () => clearInterval(interval)
    }
  }, [taskId])

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
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/upload_pdf`, {
        method: "POST",
        body: formData,
      })

      if (response.ok) {
        const data = await response.json()
        setTaskId(data.task_id)
        localStorage.setItem("ttvUploadTaskId", data.task_id)
        setUploadStatus("PDF uploaded")
      }
    } catch (error) {
      localStorage.removeItem("ttvUploadTaskId")
      setUploadStatus("Error uploading PDF. Please try again.")
    }
  }

  return (
    <div className="flex-grow flex flex-col items-center justify-center p-6">
      <div className="bg-white text-black rounded-lg p-8 w-full max-w-6xl grid grid-cols-2">
        
        <h2 className="text-2xl col-span-2 font-bold mb-4 text-center text-gray-700">Generate Script</h2>

        <div className="ml-10">
          <h2 className="text-xl font-semibold text-gray-700">Upload File</h2>
        </div>

        <div>
          <div className="mb-4">
            <div class="flex items-center justify-center w-full">
              <label
                for="dropzone-file"
                class="flex flex-col items-center justify-center w-full h-44 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100">
                <div class="flex flex-col items-center justify-center pt-5 pb-6">
                  <svg
                    class="w-8 h-8 mb-4 text-gray-500"
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 20 16">
                    <path
                      stroke="currentColor"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
                    />
                  </svg>
                  <p class="mb-2 text-sm text-gray-500">
                    <span class="font-semibold">Click to upload</span> or drag and drop
                  </p>
                <input id="dropzone-file" type="file" accept="application/pdf" onChange={handleFileChange} />
                </div>
              </label>
            </div>
          </div>

          <button
            onClick={handleUpload}
            className="w-full px-4 py-2 bg-indigo-600 text-white rounded-md mb-4 hover:bg-indigo-700 transition duration-300">
            Upload PDF
          </button>
        </div>

        {uploadStatus && <p className="mt-4 text-center text-gray-600">{uploadStatus}</p>}
      </div>
    </div>
  )
}

export default Admin
