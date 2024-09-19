import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import quizData from './quiz_data.json'; // Assuming quizData is still used

const generateRandomUsername = () => {
  const adjectives = ["happy", "lucky", "sunny", "clever", "swift"];
  const nouns = ["cat", "dog", "bird", "fish", "fox"];
  return `${adjectives[Math.floor(Math.random() * adjectives.length)]}${nouns[Math.floor(Math.random() * nouns.length)]}`;
};

function Quiz() {
  const location = useLocation();
  const navigate = useNavigate();
  const { pauseCount, playTime, selectedVideo } = location.state || { pauseCount: 0, playTime: 0, selectedVideo: '' };
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [score, setScore] = useState(0);
  const [showScore, setShowScore] = useState(false);
  const [selectedAnswer, setSelectedAnswer] = useState('');
  const [answers, setAnswers] = useState(Array(quizData.quiz.length).fill(null));

  useEffect(() => {
    if (showScore) {
      const username = generateRandomUsername();
      const data = {
        username,
        vid_name: selectedVideo,
        score,
        pause_count: pauseCount,
        play_time: playTime,
      };
      fetch('http://127.0.0.1:8000/submit_data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
        .then((response) => response.json())
        .then((data) => console.log('Success:', data))
        .catch((error) => console.error('Error:', error));
    }
  }, [showScore, pauseCount, playTime, score, selectedVideo]);

  const handleAnswerClick = (answer) => {
    setSelectedAnswer(answer);
  };

  const handleNextQuestion = () => {
    const updatedAnswers = [...answers];
    updatedAnswers[currentQuestion] = selectedAnswer;
    setAnswers(updatedAnswers);

    if (selectedAnswer === quizData.quiz[currentQuestion].correctAnswer) {
      setScore(score + 1);
    }

    setSelectedAnswer("");
    const nextQuestion = currentQuestion + 1;

    if (nextQuestion < quizData.quiz.length) {
      setCurrentQuestion(nextQuestion);
      setSelectedAnswer(updatedAnswers[nextQuestion]);
    } else {
      setShowScore(true);
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
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-xl p-8 bg-white shadow-lg rounded-lg">
        {showScore ? (
          <div className="text-center">
            <h2 className="text-3xl font-bold mb-4">Quiz Completed!</h2>
            <p className="text-xl">You scored {score} out of {quizData.quiz.length}</p>
            <div className="mt-6">
              <h3 className="text-2xl font-bold">Video Analytics</h3>
              <p className="text-lg">Number of pauses: {pauseCount}</p>
              <p className="text-lg">Total time video played: {playTime} seconds</p>
            </div>
            <button
              onClick={() => navigate('/')}
              className="mt-6 py-3 px-4 bg-indigo-600 text-white font-semibold rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              Return to Home
            </button>
          </div>
        ) : (
          <>
            <div className="mb-6">
              <h2 className="text-2xl font-bold mb-4">
                Question {currentQuestion + 1}/{quizData.quiz.length}
              </h2>
              <div className="text-lg">{quizData.quiz[currentQuestion].question}</div>
            </div>
            <div className="space-y-4">
              {quizData.quiz[currentQuestion].options.map((option, index) => (
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
                {currentQuestion + 1 === quizData.quiz.length ? "Finish Quiz" : "Next"}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default Quiz;
