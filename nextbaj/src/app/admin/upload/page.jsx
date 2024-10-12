"use client"

import { useState } from "react"
import ImageComp from "./ImageComp"

const LANGUAGES = ["english", "hindi", "marathi", "tamil", "telugu", "kannada", "malayalam", "bengali", "gujarati", "punjabi"]

function Admin() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [uploadStatus, setUploadStatus] = useState("")
  const [selectedCard, setSelectedCard] = useState(0)
  const [numberOfSlides, setNumberOfSlides] = useState(10)
  const [processId, setProcessId] = useState()
  const [height, setHeight] = useState(960)
  const [width, setWidth] = useState(540)
  const [captions, setCaptions] = useState(true)
  const [languages, setLanguages] = useState(["English"])

  const [scripts, setScripts] = useState([])
  const [images, setImages] = useState()

  const handleFileChange = e => {
    setSelectedFile(e.target.files[0])
  }

  const handleUpload = async () => {
    // if (!selectedFile) {
    //   setUploadStatus("Please select a PDF file.")
    //   return
    // }

    if (numberOfSlides < 1) {
      setUploadStatus("Please enter a valid number of slides.")
      return
    }

    const formData = new FormData()
    formData.append("slides", numberOfSlides)
    formData.append("pdf", selectedFile)

    try {
      // const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/get_script`, {
      //   cache: "force-cache",
      //   method: "POST",
      //   body: formData,
      // })

      // if (response.ok) {
      //   const data = await response.json()
      //   console.log(data)
      //   setScripts(data.scripts)
      //   setProcessId(data.processId)
      // }

      setScripts([
        {
          Title: "Entry and Renewal Age",
          Script:
            "The entry age for our insurance policies is set at 18 to 65 years for adults and 3 months to 21 years for dependent children. Our policies typically come with a lifetime renewal benefit, ensuring continued coverage under normal circumstances, barring issues related to fraud or moral hazard.",
        },
        {
          Title: "Hospital Cash Daily Allowance Policy",
          Script:
            "Our Hospital Cash Daily Allowance Policy protects you and your family from financial burdens during hospitalization. It pays a daily benefit amount to cover incidental expenses, providing peace of mind when you need it most. Coverage duration can be for 30 or 60 days within the policy period.",
        },
      ])
      setProcessId("1234")
    } catch (error) {
      localStorage.removeItem("ttvUploadTaskId")
      setUploadStatus("Error uploading PDF. Please try again.")
    }
  }

  return (
    <div className="flex-grow flex flex-col items-center justify-center p-6">
      <div className="bg-white text-black rounded-lg p-8 w-full max-w-6xl">
        <h2 className="text-2xl col-span-2 font-bold mb-10 text-center text-gray-700">Create Video</h2>

        <div className="mb-5">
          <h2 className="text-xl font-semibold text-gray-700">Upload File</h2>
        </div>

        <div>
          <div className="mb-4">
            <div className="mb-4 grid grid-cols-2 gap-4">
              <div className="flex flex-row">
                {/* New Numeric Input for Number of Slides */}
                <label htmlFor="number-of-slides" className="my-auto mr-2 block text-lg text-gray-700 font-semibold">
                  Number of Slides:
                </label>
                <input
                  id="number-of-slides"
                  type="number"
                  value={numberOfSlides}
                  onChange={e => setNumberOfSlides(e.target.value)}
                  className="mt-1 block border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  min="1" // Minimum value for slides
                />
              </div>
              <div className="flex flex-row">
                <label htmlFor="number-of-slides" className="my-auto block text-lg text-gray-700 font-semibold">
                  Approximate Time:
                </label>
                <label htmlFor="number-of-slides" className="ml-2 my-auto block text-lg text-gray-700">
                  {numberOfSlides * 15} secs
                </label>
              </div>
            </div>
            <div className="flex items-center justify-center w-full">
              <label
                htmlFor="dropzone-file"
                className="flex flex-col items-center justify-center w-full h-44 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100">
                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                  <svg
                    className="w-8 h-8 mb-4 text-gray-500"
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 20 16">
                    <path
                      stroke="currentColor"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
                    />
                  </svg>
                  <p className="mb-2 text-sm text-gray-500">
                    <span className="font-semibold">Click to upload</span> or drag and drop
                  </p>
                  <input id="dropzone-file" type="file" accept="application/pdf" onChange={handleFileChange} />
                </div>
              </label>
            </div>
          </div>

          <button
            onClick={handleUpload}
            className="w-full px-4 py-2 bg-indigo-600 text-white rounded-md mb-4 hover:bg-indigo-700 transition duration-300">
            Generate Script
          </button>
        </div>

        {scripts.length != 0 && (
          <div>
            <div className="overflow-x-auto whitespace-nowrap mb-4">
              {scripts.map((card, index) => (
                <div
                  key={index}
                  onClick={() => setSelectedCard(index)}
                  className={`inline-block p-2 m-1 border rounded-lg cursor-pointer ${
                    selectedCard === index ? "bg-blue-500 text-white" : "bg-gray-200"
                  }`}>
                  {card.Title}
                </div>
              ))}
            </div>

            <textarea
              id="message"
              rows="4"
              className="mb-4 block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              placeholder="Write your thoughts here..."
              value={scripts[selectedCard]["Script"]}
              onChange={e => {
                let temp = [...scripts]
                temp[selectedCard]["Script"] = e.target.value
                setScripts(temp)
              }}></textarea>

            <div className="flex flex-row mb-4 gap-3">
              <div className="inline-flex rounded-md mr-3" role="group">
                <button
                  onClick={() => {
                    setWidth(540)
                    setHeight(960)
                  }}
                  type="button"
                  className="px-4 py-2 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-s-lg hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:bg-gray-800 dark:border-gray-700 dark:text-white dark:hover:text-white dark:hover:bg-gray-700 dark:focus:ring-blue-500 dark:focus:text-white">
                  Vertical
                </button>
                <button
                  onClick={() => {
                    setWidth(950)
                    setHeight(540)
                  }}
                  type="button"
                  className="px-4 py-2 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-e-lg hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700 dark:bg-gray-800 dark:border-gray-700 dark:text-white dark:hover:text-white dark:hover:bg-gray-700 dark:focus:ring-blue-500 dark:focus:text-white">
                  Horizontal
                </button>
              </div>

              <label htmlFor="height" className="my-auto block text-gray-700">
                Height
              </label>
              <input
                id="height"
                type="number"
                value={height}
                onChange={e => setHeight(e.target.value)}
                className="mt-1 block w-24 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                min="1" // Minimum value for height
              />

              <label htmlFor="width" className="my-auto block text-gray-700 ml-3">
                Width
              </label>
              <input
                id="width"
                type="number"
                value={width}
                onChange={e => setWidth(e.target.value)}
                className="mt-1 block w-24 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                min="1" // Minimum value for width
              />
            </div>

            <button
              onClick={() => {
                setImages([])
              }}
              className="w-full px-4 py-2 bg-indigo-600 text-white rounded-md mb-4 hover:bg-indigo-700 transition duration-300">
              Generate Images
            </button>
          </div>
        )}

        {images && (
          <>
            <div className="overflow-x-auto whitespace-nowrap mb-4">
              {scripts.length != 0 &&
                scripts.map((card, index) => (
                  <ImageComp key={index} card={card} ind={index} processId={processId} height={height} width={width} />
                ))}
            </div>

            <div className="flex mb-4">
              <div className="ml-4 flex items-center rounded-md border-2 py-1 px-2">
                <input
                  id="captions"
                  type="checkbox"
                  className="mr-2"
                  checked={captions}
                  onChange={e => setCaptions(e.target.checked)}
                />
                <label htmlFor="captions" className="text-gray-700">
                  Captions
                </label>
              </div>

              <div className="ml-4 grid grid-cols-9 gap-4 rounded-md border-2 py-1 px-2">
                {LANGUAGES.map((language, index) => (
                  <div className="flex flex-row" key={index}>
                    <input
                      id={`language-${index}`}
                      type="checkbox"
                      className="mr-2 my-auto"
                      checked={languages.includes(language)}
                      onChange={e => {
                        if (e.target.checked) {
                          setLanguages([...languages, language])
                        } else {
                          setLanguages(languages.filter(l => l !== language))
                        }
                      }}
                    />
                    <label htmlFor={`language-${index}`} className="my-auto text-gray-700">
                      {language.charAt(0).toUpperCase() + language.slice(1)}
                    </label>
                  </div>
                ))}
              </div>
            </div>

            <button
              onClick={() => {
                fetch(`${process.env.NEXT_PUBLIC_API_URL}/generate_video`, {
                  method: "POST",
                  headers: {
                    "Content-Type": "application/json",
                  },
                  body: JSON.stringify({
                    processId: processId,
                    scripts: scripts,
                    captions: captions,
                    languages: languages,
                  }),
                })
                console.log("Generate Video")
              }}
              className="w-full px-4 py-2 bg-indigo-600 text-white rounded-md mb-4 hover:bg-indigo-700 transition duration-300">
              Generate Video
            </button>
          </>
        )}

        {uploadStatus && <p className="mt-4 text-center text-gray-600">{uploadStatus}</p>}
      </div>
    </div>
  )
}

export default Admin
