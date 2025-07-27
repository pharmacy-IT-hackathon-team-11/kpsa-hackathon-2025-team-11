
import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './MyPage.css';
import { useNavigate } from 'react-router-dom';

let user_id = localStorage.getItem('user_id')
let user_password = localStorage.getItem('user_password')

function MyPage({isLoggedin}) {
  const usenavigate = useNavigate()
  return (
    isLoggedin?
    (<div className="container mt-5">
      
      <div className="row">
        <div className="col-md-4">
          <div className="card">
            <h1 style={{fontWeight:'900'}}>MYPAGE</h1>
            <img src="/ham_profile.png" className="card-img-top" alt="profile"/>
            <div className="card-body text-center">
              <h5 className="card-title"style={{fontWeight:'900'}}>{user_id}</h5>
              <p className="card-text">Golden Hamster</p>
            </div>
          </div>
        </div>
        <div className="col-md-8">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">프로필 정보</h5>
              <hr />
              <div className="row">
                <div className="col-sm-3">
                  <h6 className="mb-0">User ID</h6>
                </div>
                <div className="col-sm-9 text-secondary">
                  {user_id}
                </div>
              </div>
              <hr />
              <div className="row">
                <div className="col-sm-3">
                  <h6 className="mb-0">비밀번호</h6>
                </div>
                <div className="col-sm-9 text-secondary">
                  <button className="btn btn-primary btn-sm" onClick={()=>{usenavigate('/login')}}>Change Password</button>
                </div>
              </div>
              <hr />
              <div className="row">
                <div className="col-sm-3">
                  <h6 className="mb-0">종족</h6>
                </div>
                <div className="col-sm-9 text-secondary">
                  Golden Hamster
                </div>
              </div>
              <hr />
              <div className="row">
                <div className="col-sm-3">
                  <h6 className="mb-0">호감음식</h6>
                </div>
                <div className="col-sm-9 text-secondary">
                  Sunflower Seeds
                </div>
              </div>
              <hr />
              <div className="row">
                <div className="col-sm-3">
                  <h6 className="mb-0">취미</h6>
                </div>
                <div className="col-sm-9 text-secondary">
                  Running on the wheel
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>):
  (
    <>
      <div id='title' className='blackbg' style={{backgroundColor:'#999'}}>
        <img src="/hamstercrew(tp).png" alt="전햄연로고" style={{ width: '200px' }} />
        <h1 id='greeting'>아직 가입하지 않았어요! <br /> 로그인하고 오세요</h1>
      </div>
    </>
  
  )
  );
};

export default MyPage;
