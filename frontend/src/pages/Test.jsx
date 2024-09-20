import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Test() {
  const [taskId, setTaskId] = useState(null);
  const [taskStatus, setTaskStatus] = useState('');

  
  const startTask = async () => {
    try {
      const response = await axios.post('http://localhost:8000/start-task');
      setTaskId(response.data.task_id);
      setTaskStatus('Task started...');
    } catch (error) {
      console.error('Error starting task:', error);
    }
  };

  
  useEffect(() => {
    if (taskId) {
      const interval = setInterval(async () => {
        try {
          const statusResponse = await axios.get(
            `http://localhost:8000/check-task-status/${taskId}`
          );
          setTaskStatus(statusResponse.data.status);

          
          if (statusResponse.data.status === 'completed') {
            clearInterval(interval);
          }
        } catch (error) {
          console.error('Error fetching task status:', error);
        }
      }, 2000); 

      return () => clearInterval(interval); 
    }
  }, [taskId]);

  return (
    <div>
      <h1>Long Running Task</h1>
      <button onClick={startTask}>Start Task</button>
      {taskId && <p>Task ID: {taskId}</p>}
      <p>Status: {taskStatus}</p>
    </div>
  );
}

export default Test;
