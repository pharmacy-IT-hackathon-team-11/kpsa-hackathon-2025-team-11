import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter, Routes, Route} from 'react-router-dom'
import React, { useState } from 'react';
import ScrollToTop from './scrollToTop'; //스크롤을 위로 올려준다.
import App from './App';
import Login from './Pages/Login';
import Link from './Link';
import Signup from './Pages/Signup';
import MyPage from './Pages/MyPage';
import Message from './Pages/Message';
import Back from './Pages/backcheck'
import Home from './Pages/home'
import Analyze from './Pages/Analyze';
import Complete from './Pages/Complete'

function Routing({ isLoggedin, handleLoginSuccess }) {

    return ( //app에는 결과값 전달, login에는 성공 확인 함수 전달.
    <>
        <ScrollToTop />
        <Routes>
            <Route path="/" element={<App isLoggedin={isLoggedin} handleLoginSuccess={handleLoginSuccess}/>} /> 
            <Route path="/login" element={<Login handleLoginSuccess={handleLoginSuccess}/>} />
            <Route path="/link" element={<Link />} />
            <Route path="/signup" element={<Signup handleLoginSuccess={handleLoginSuccess}/>} />
            <Route path="/home" element={<Home />} />
            <Route path="/mypage" element={<MyPage isLoggedin={isLoggedin}/>} />
            <Route path="/back" element={<Back />} />
            <Route path="/result" element={<Analyze />}/>
            <Route path="/signup/complete" element={<Complete />}/>
        </Routes>
    </>
    )
}

export default Routing