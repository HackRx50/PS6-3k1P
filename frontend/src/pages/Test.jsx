"use client"

import { useNavigate } from "react-router-dom";



export default function BarChartHero() {

  const navigate = useNavigate();

  const handleTakeQuiz = () => {
    navigate("/quiz", {
      state: { selectedVideo:"Loan-Care-Brochure.mp4", pauseCount:0, playTime:0 },
    });
  };
  

  return (
    <div>
      <div className="w-96 p-4 bg-white shadow-md rounded-lg overflow-hidden cursor-pointer hover:shadow-xl transition-shadow">
        <button onClick={()=>handleTakeQuiz()}>Quiz</button>
      </div>
    </div>
  )
}
