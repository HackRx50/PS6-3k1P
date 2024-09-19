import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './index.css';
import User from './pages/User';
import Admin from './pages/Admin';
import App from './App';
import Quiz from './pages/Quiz';
import Analytics from './pages/Analytics';
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <Routes>
          <Route path='/' element={<App/>}/>
          <Route path='/quiz' element={<Quiz/>}/>
          <Route path="/user" element={<User />} />
          <Route path="/admin" element={<Admin />} />  
          <Route path="/analytics" element={<Analytics />} />  
      </Routes>
    </Router>
  </React.StrictMode>
);
