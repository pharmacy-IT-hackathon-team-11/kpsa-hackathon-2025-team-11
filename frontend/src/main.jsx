
import { StrictMode, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import './index.css';
import 'bootstrap/dist/css/bootstrap.min.css';

import Navigation from './Navigation.jsx';
import Routing from './routing.jsx';
import Modal from './Modal.jsx';
import { ModalContext } from './ModalContext.jsx';
import Footer from './Footer.jsx'


// 앱의 모든 상태를 관리하는 총사령관 컴포넌트
function Main() {
  // 모달의 상태를 여기서 유일하게 관리합니다.
  const [isModalOpen, setIsModalOpen] = useState(false);
  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  const [isMsgOpen, setIsMsgOpen] = useState(false);
  const openMsg = () => setIsMsgOpen(true);
  const closeMsg = () => setIsMsgOpen(false);

  const [isLoggedin, handleLoginSuccess] = useState(false)

  return (
    // 방송 시스템 가동! openModal, closeModal 정보를 방송합니다.
    <ModalContext.Provider value={{ openModal, closeModal, openMsg, closeMsg, isLoggedin }}>
      <BrowserRouter>
        <Navigation isLoggedin={isLoggedin} handleLoginSuccess={handleLoginSuccess}/>
        <Routing isLoggedin={isLoggedin} handleLoginSuccess={handleLoginSuccess}/>
        {/* 모달의 렌더링 여부는 여기서만 결정합니다. */}
        {isModalOpen && <Modal />}
        {isMsgOpen && <Message />}
        <Footer />
      </BrowserRouter>
    </ModalContext.Provider>
  );
}

// 앱의 유일한 진입점입니다.
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Main />
  </StrictMode>
);

import './index.css'
import App from './App.jsx'




import React from 'react';
import Message from './Pages/Message.jsx';

