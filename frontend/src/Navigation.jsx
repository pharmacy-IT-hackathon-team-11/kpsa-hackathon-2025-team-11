import React, { useContext } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import { useNavigate } from 'react-router-dom';
import { ModalContext } from './ModalContext.jsx';
import './App.css'
import { width } from '@fortawesome/free-brands-svg-icons/fa42Group';

function Navigation({isLoggedin, handleLoginSuccess}) {
  const navigate = useNavigate();
  // '공구함'에서 '망치(openModal)'만 정확히 꺼내옵니다.
  const { openModal } = useContext(ModalContext);
  const { openMsg } = useContext(ModalContext)

  const token = localStorage.getItem('token')

  function logOut(){
    console.log('로그아웃')
    const handleLogout = async () => {
      try {
        const response = await fetch('https://6mip5m9jtv.us-east-1.awsapprunner.com/api/v1/auth/logout', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`, // 여기 accessToken은 로그인 때 받은 토큰. 이거 넣어주면 아마 오류 안 날 거임
            'accept': 'application/json'
          }
        });
        if (response.ok) {
          alert('로그아웃 완료!');
          // 토큰도 localStorage 등에서 삭제해줘야 함
          localStorage.removeItem('accessToken');
          // 상태도 변경 (예: 로그인 상태 false로)
          handleLoginSuccess(false);
          navigate('/login');
        } else {
          alert('로그아웃 실패');
        }
      } catch (error) {
        console.error('로그아웃 중 오류:', error);
      }
    };
    handleLogout()
  }

  return (
    <nav className="navbar navbar-expand-lg bg-body-tertiary white" style={{backgroundColor:'white'}}>
      <div className="container-fluid">
        <a className="navbar-brand" href="#" onClick={() => navigate('/')} style={{fontWeight:900, fontSize:'bigger'}}>
          <img src="/dnable_logo.png" alt="" style={{height:'18px', marginBottom:'3px'}}/>
        </a>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon" />
        </button>
        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <li className="nav-item">
              <a className="nav-link active" href='#' aria-current="page" onClick={() => navigate('/back')}>
                파트너십문의
                
              </a>
            </li>
            <li className="nav-item dropdown">
              <a
                className="nav-link dropdown-toggle"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                앱 다운로드
              </a>
              <ul className="dropdown-menu">
                <li>
                  <a className="dropdown-item" href="#" onClick={() => console.log('hahaha')}>
                    ios
                  </a>
                </li>
                <li>
                  <a className="dropdown-item" href="#">
                    android
                  </a>
                </li>
                <li>
                </li>
              </ul>
            </li>
            <li className="nav-item">
              <a className="nav-link disabled" aria-disabled="true">
                Disabled
              </a>
            </li>
          </ul>
          {isLoggedin ? (<button className="btn btn-outline-success" style={{width:'200px', whiteSpace:'nowrap'}} onClick={() => {navigate('/home')
            handleLoginSuccess(true)
            logOut()
          }}>
              Logout
            </button>):(<button className="btn btn-outline-success" style={{width:'200px', whiteSpace:'nowrap'}} onClick={() => navigate('/login')}>
              Login / Signup
            </button>)}
            
        </div>
      </div>
    </nav>
  );
}

export default Navigation;