// frontend/src/Complete.jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import './complete.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import { useNavigate } from 'react-router-dom';


function Complete() {

    const navigate = useNavigate()

    return (
        <>
        <div className="wrap">
            <img className='check' src="/check.png" alt="check" />
            <h2>회원가입 완료</h2>
            <p>모든 회원가입 절차가 완료되었습니다.</p>
            <p>로그인 후 모든 서비스를 이용할 수 있습니다.</p>
            <div className="btn">
                <button className='login btn btn-primary' onClick={()=>{navigate('/login')}}>로그인</button>
                <button className='main btn btn-light' onClick={()=>navigate('/')} style={{border:'1px solid #ccc'}}>메인으로</button>
            </div>
        </div>
        </>
    )
}

export default Complete;