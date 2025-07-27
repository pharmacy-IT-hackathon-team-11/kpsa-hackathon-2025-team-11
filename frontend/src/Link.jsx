
import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';

let user_id = localStorage.getItem('user_id')
let user_password = localStorage.getItem('user_password')

function Link() {

  return (
    <div className='mypage'>
      <br />
        <h1 style={{fontWeight:'900'}}>MYPAGE</h1>

        <img src="/ham_profile.png" width={'200px'} alt="" />

      <div>당신의 id: {user_id}</div>
      <div>당신의 비밀번호: {user_password}</div>

    </div>
  )
}


export default Link
