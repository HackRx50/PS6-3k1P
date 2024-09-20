import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Test() {
  const [taskId, setTaskId] = useState(null);
  const [taskStatus, setTaskStatus] = useState('');

  // Function to start the task
  const startTask = async () => {
    try {
      const response = await axios.post('http://localhost:8000/start-task');
      setTaskId(response.data.task_id);
      setTaskStatus('Task started...');
    } catch (error) {
      console.error('Error starting task:', error);
    }
  };

  // Polling the task status every 5 seconds
  useEffect(() => {
    if (taskId) {
      const interval = setInterval(async () => {
        try {
          const statusResponse = await axios.get(
            `http://localhost:8000/check-task-status/${taskId}`
          );
          setTaskStatus(statusResponse.data.status);

          // Stop polling when task is complete
          if (statusResponse.data.status === 'completed') {
            clearInterval(interval);
          }
        } catch (error) {
          console.error('Error fetching task status:', error);
        }
      }, 2000); // Poll every 5 seconds

      return () => clearInterval(interval); // Clean up on unmount
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
