"use client";

import { useSearchParams } from "next/navigation"; // Import useSearchParams for query params
import { useEffect, useState } from "react";
import Navbar from "@/components/Navbar";

export default function UserQuiz() {
  const searchParams = useSearchParams(); // Access search parameters
  const video_name = searchParams.get("video_name"); // Get video_name from search params

  const [quizData, setQuizData] = useState([]); // Initialize quizData as an array
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState("");
  const [answers, setAnswers] = useState([]);
  const [score, setScore] = useState(0);
  const [showScore, setShowScore] = useState(false);

  useEffect(() => {
    console.log("Video Name:", video_name); // Log the video name
    if (video_name) {
      fetch(`${process.env.NEXT_PUBLIC_API_URL}/get_quiz?video_name=${video_name}`)
        .then((response) => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then((data) => {
          setQuizData(data.quiz); 
          console.log("Fetched Quiz Data:", data.quiz); // Log the fetched quiz data
        })
        .catch((error) => {
          console.error('There was a problem with the fetch operation:', error);
        });
    }
  }, [video_name]);

  const handleAnswerClick = (answer) => {
    setSelectedAnswer(answer);
  };

  const handleNextQuestion = async () => {
    const updatedAnswers = [...answers];
    updatedAnswers[currentQuestion] = selectedAnswer;
    setAnswers(updatedAnswers);

    if (selectedAnswer === quizData[currentQuestion]?.correctAnswer) {
      setScore(score + 1);
    }

    setSelectedAnswer("");
    const nextQuestion = currentQuestion + 1;

    if (nextQuestion < quizData.length) {
      setCurrentQuestion(nextQuestion);
      setSelectedAnswer(updatedAnswers[nextQuestion]);
    } else {
      setShowScore(true);
      await submitScoreData(); // Submit score data when quiz is completed
    }
  };

  const submitScoreData = async () => {
    const username = "your_username"; // Replace with actual username logic
    const data = {
      username,
      vid_name: video_name,
      score,
    };

    try {
      await fetch(`${process.env.NEXT_PUBLIC_API_URL}/submit_score_data`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
    } catch (error) {
      console.error("Error submitting score data:", error);
    }
  };

  const handlePreviousQuestion = () => {
    const prevQuestion = currentQuestion - 1;
    if (prevQuestion >= 0) {
      setCurrentQuestion(prevQuestion);
      setSelectedAnswer(answers[prevQuestion]);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-r from-blue-50 to-blue-100">
      <Navbar />
      <div className="flex-grow flex flex-col items-center justify-center p-8">
        {quizData.length > 0 && (
          <div className="w-full max-w-xl p-8 bg-white shadow-lg rounded-lg">
            {showScore ? (
              <div className="text-center">
                <h2 className="text-3xl font-bold mb-4 text-black">Quiz Completed!</h2>
                <p className="text-xl text-black">
                  You scored {score} out of {quizData.length}
                </p>
              </div>
            ) : (
              <>
                <div className="mb-6">
                  <h2 className="text-2xl font-bold mb-4 text-black">
                    Question {currentQuestion + 1}/{quizData.length}
                  </h2>
                  <div className="text-lg text-black">
                    {quizData[currentQuestion]?.question}
                  </div>
                </div>
                <div className="space-y-4 text-black">
                  {quizData[currentQuestion]?.options.map((option, index) => (
                    <button
                      key={index}
                      className={`w-full py-3 px-4 text-left bg-gray-200 hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 rounded-md ${
                        selectedAnswer === option ? "bg-indigo-300" : ""
                      }`}
                      onClick={() => handleAnswerClick(option)}
                    >
                      {option}
                    </button>
                  ))}
                </div>
                <div className="flex justify-between mt-6">
                  <button
                    onClick={handlePreviousQuestion}
                    disabled={currentQuestion === 0}
                    className="py-3 px-4 bg-indigo-600 text-white font-semibold rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:bg-gray-400"
                  >
                    Previous
                  </button>
                  <button
                    onClick={handleNextQuestion}
                    disabled={!selectedAnswer}
                    className="py-3 px-4 bg-indigo-600 text-white font-semibold rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:bg-gray-400"
                  >
                    {currentQuestion + 1 === quizData.length ? "Finish Quiz" : "Next"}
                  </button>
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
