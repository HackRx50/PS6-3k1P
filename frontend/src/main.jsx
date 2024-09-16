import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './index.css';
import User from './pages/user';
import Admin from './pages/Admin';
import App from './App';
import Quiz from './pages/Quiz';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <Routes>
          <Route path='/' element={<App/>}/>
          <Route path='/quiz' element={<Quiz/>}/>
          <Route path="/user" element={<User />} />
          <Route path="/admin" element={<Admin />} />  
      </Routes>
    </Router>
  </React.StrictMode>
);
