
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './index2.css';
import Signup from './Signup';
localStorage.setItem('key', JSON.stringify({ username: 'hamsteradmin', password: 'hamstersekai123' })); // For testing purposes

function Login({handleLoginSuccess}) {
  const [userID, setUserID] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  let [profile, setProfile] = useState('약사')

  const data = {
  user_id: userID,
  password: password
}


  const handleLogin = async (e) => {
  e.preventDefault();

  const data = {
    user_id: userID,
    password: password
  };

  try {
    const response = await fetch('https://6mip5m9jtv.us-east-1.awsapprunner.com/api/v1/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (response.ok) {
      console.log('로그인 됐어')
      const token = result.token.access_token;
      localStorage.setItem('token', token);

      // 👇 로그인 성공 후 유저 정보 가져오기
      const userRes = await fetch('https://6mip5m9jtv.us-east-1.awsapprunner.com/api/v1/auth/me', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    const userData = await userRes.json();

    if (userRes.ok) {
      console.log('유저 정보:', userData);
      // 여기에 setUserInfo(userData) 같은 것도 가능
    }


      alert(`${userID}님, 로그인이 완료되었습니다!`);
      handleLoginSuccess(true); // 로그인 상태 변경
    
      navigate('/home');
    } else {
      console.error('서버 응답 오류:', result);
      alert(result.message || '로그인에 실패했어요.');
      navigate('/');
    }
  } catch (err) {
    console.error('요청 실패:', err);
    alert('네트워크 오류로 로그인 실패!');
  }

  console.log(data);
};




  return (
    
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h2 className="card-title text-center mb-4" style={{fontWeight:'bold'}}>로그인</h2>
              <p style={{fontWeight:'normal', fontSize:'small'}}>로그인 유형을 선택해주세요.</p>
              <div className="buttons" style={{display:'flex', justifyContent:'space-between'}}>
                  <button className={profile === '약사' ? 'btn btn-primary':'btn btn-light'} style={{width:'50%'}} onClick={()=>setProfile('약사')}>약사</button>
                  <button className={profile === '관리자' ? 'btn btn-primary':'btn btn-light'} style={{width:'50%', border:'1px solid #ccc'}} onClick={()=>setProfile('관리자')}>관리자</button>
              </div>
              <form onSubmit={handleLogin}>
                <div className="mb-2">
                  <input
                    type="text"
                    className="form-control"
                    id="username"
                    value={userID}
                    onChange={(e) => setUserID(e.target.value)}
                    placeholder='아이디'
                  />
                </div>
                
                <div className="mb-3">
                  <input
                    type="password"
                    className="form-control"
                    id="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder='비밀번호'
                  />
                </div>
                <div className="login-setting" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <label style={{ display: 'flex', alignItems: 'center', fontWeight: 'normal', fontSize: 'small' }}>
                  <input type="checkbox" style={{ marginRight: '5px', margin:'0 5px' }} />
                  아이디 자동저장
                </label>
                <p style={{ margin: 0, fontWeight: 'normal', fontSize: 'small' }}>아이디 찾기 / 비밀번호 찾기</p>
              </div>
                
                <div className="d-grid">
                  <button type="submit" className="btn btn-primary">Login</button>
                </div>

                <br />
                <p style={{fontWeight:'normal', fontSize:'small'}}>아직 회원이 아니신가요?</p>
                <div className="d-grid">
                  <button type="button" onClick={()=>navigate('/signup')} className="btn btn-light" style={{border:'1px solid #ccc'}}>회원가입</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
