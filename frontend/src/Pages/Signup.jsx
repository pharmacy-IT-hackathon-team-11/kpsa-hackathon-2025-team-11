
import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './index2.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function Signup({handleLoginSuccess}) {

const navigate = useNavigate() //navigate 함수로 정의하기.

const [userId, setUserId] = useState('');
const [password, setPassword] = useState('');
const [passwordCheck, check] = useState('')
const [name, setName] = useState('')
const [phoneNumber, setPhoneNumber] = useState('');
const [licenseId, setLicenseId] = useState('');
const [pharmacyName, setPharmacyName] = useState('');
const [pharmacyAddress, setPharmacyAddress] = useState('');





const handleSubmit = async (e) => {
e.preventDefault();

// 간단한 유효성 검사
if (!userId || !password || !phoneNumber || !licenseId) {
    alert('필수 항목이 비어 있어!');
    return;
}

const data = {
    full_name: name,
    pharmacy_road_address: pharmacyAddress,
    pharmacy_position_x: 0, // 위치값은 나중에 GPS나 주소 API로!
    pharmacy_position_y: 0,
    phone_number: phoneNumber,
    license_id: licenseId,
    pharmacy_name: pharmacyName,
    user_id: userId,
    password: password
};

try {
    const response = await fetch('https://6mip5m9jtv.us-east-1.awsapprunner.com/api/v1/auth/register', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
    });

    const result = await response.json();

    if (response.ok) {
    alert(`${userId}님, 가입 성공했어요!`);
    handleLoginSuccess(true); // 로그인 상태 변경
    const token = result.token.access_token;
    localStorage.setItem('token', token);
    navigate('/signup/complete');
    } else {
    console.error('서버 응답 오류:', result);
    alert(result.message || '가입에 실패했어요.');
    navigate('/home');
    }

    } catch (err) {
        console.error('요청 실패:', err);
        alert('네트워크 오류로 가입 실패!');
    }
    console.log(data)
};

function signupCheck() {
    if (password !== passwordCheck) {
    alert('비밀번호가 서로 다릅니다!');
    return;
    }
}


    return (
        <div className="container py-5">
        <div className="row justify-content-center">
            <div className="col-md-8" style={{width:'600px'}}>
            <div className="card">
                <div className="card-body">
                <h2 className="card-title text-center mb-4" style={{fontWeight:'bold'}}>회원가입</h2>
                <form onSubmit={handleSubmit}>
                    <div className="form1">
                    <label className="form-label info">로그인 정보</label>
                    </div>
                    <div className="form1">
                    <label htmlFor="name" className="form-label">id</label>
                    <input
                        type="text"
                        className="form-control"
                        id="id"
                        value={userId}
                        onChange={(e) => setUserId(e.target.value)}
                        placeholder='중복 불가'
                    />
                    </div>

                    <div className="form1">
                    <label htmlFor="password" className="form-label">비밀번호</label>
                    <input
                        type="password"
                        className="form-control"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder='비밀번호는 8자 이상 작성하세요'
                    />
                    </div>

                    <div className="form1">
                    <label htmlFor="password-check" className="form-label">비밀번호 확인</label>
                    <input
                        type="password"
                        className="form-control"
                        id="password-check"
                        value={passwordCheck}
                        onChange={(e) => check(e.target.value)}
                    />
                    </div>
                    <hr />
                    <label className="form-label info">회원정보</label>
                    <div className="form1">
                    <label htmlFor="name" className="form-label">이름</label>
                    <input
                        type="text"
                        className="form-control"
                        id="name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />
                    </div>
                    <div className="form1">
                    <label htmlFor="name" className="form-label">전화번호</label>
                    <input
                        type="tel"
                        className="form-control"
                        id="phoneNumber"
                        value={phoneNumber}
                        onChange={(e) => setPhoneNumber(e.target.value)}
                    />
                    </div>
                    <div className="form1">
                    <label htmlFor="name" className="form-label">약사면허번호</label>
                    <input
                        type="text"
                        className="form-control"
                        id="licenseId"
                        value={licenseId}
                        onChange={(e) => setLicenseId(e.target.value)}
                        placeholder='중복 불가'
                    />
                    </div>
                    <div className="form1">
                    <label htmlFor="name" className="form-label">약국 주소</label>
                    <input
                        type="text"
                        className="form-control"
                        id="pharmacyAddress"
                        value={pharmacyAddress}
                        onChange={(e) => setPharmacyAddress(e.target.value)}
                    />
                    </div>
                    <div className="form1">
                    <label htmlFor="name" className="form-label">약국명</label>
                    <input
                        type="text"
                        className="form-control"
                        id="pharmacyName"
                        value={pharmacyName}
                        onChange={(e) => setPharmacyName(e.target.value)}
                    />
                    </div>
                    <hr />
                    <div className="form1">
                    <label className="form-label info">가입 약관 동의</label>
                    </div>
                <div className="login-setting2">
                    <label style={{ display: 'flex', alignItems: 'center', fontWeight: 'normal', fontSize: 'small' }}>
                    <input type="checkbox" style={{ marginRight: '5px', margin:'0 5px' }} />
                    모든 약관에 동의합니다.
                    </label>
                    <label style={{ display: 'flex', alignItems: 'center', fontWeight: 'normal', fontSize: 'small' }}>
                    <input type="checkbox" style={{ marginRight: '5px', margin:'0 5px' }} />
                    디에너블 약관에 동의합니다. (필수)
                    </label>
                    <label style={{ display: 'flex', alignItems: 'center', fontWeight: 'normal', fontSize: 'small' }}>
                    <input type="checkbox" style={{ marginRight: '5px', margin:'0 5px' }} />
                    개인정보 수집 및 이용에 동의합니다. (필수)
                    </label>
                    <label style={{ display: 'flex', alignItems: 'center', fontWeight: 'normal', fontSize: 'small' }}>
                    <input type="checkbox" style={{ marginRight: '5px', margin:'0 5px' }} />
                    마케팅 활용 및 광고성 정보 수신에 동의합니다. (선택)
                    </label>
                </div>

                    <div className="d-grid">
                    <button type="submit" className="btn btn-primary" style={{marginTop:'20px'}} onClick={()=>{signupCheck}}>가입하기</button>
                    </div>
                </form>
                <div className="text-center mt-3">
                    <p>이미 계정이 있으신가요? <Link to="/login">로그인</Link></p>
                </div>
                </div>
            </div>
            </div>
        </div>
        </div>
    );
    }

    export default Signup;
