import './Analyze.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import { useState, useEffect } from 'react'

function Analyze(){

    let name = '김지은'
    
    return(
        <div className="fullbody">

        
        <div className='analyze-body'>
            <h1>분석 결과</h1>
            <div className="containers">
                <div className="left">
                    <form action="">
                        <label>이름<input type="text" /></label>
                        <label>주민번호<input type="text" /></label>
                        <label>연락처<input type="tel" /></label>
                        <label>접수 일자<input type="date" /></label>
                        <label>현재 복용 중인 약물 및 기저질환<textarea name="" id=""></textarea></label>
                    </form>
                <button>결과보기</button>
                </div>
                <div className="right">
                    <div className="a-div"><h4>{name}님 검사 결과</h4>
                    <table className='result-a'>
                        <thead>
                            <tr>
                            <th>유전자</th>
                            <th>SNP (변이)</th>
                            <th>유전형</th>
                            <th>관련 영양소</th>
                            <th>권장 영양제</th>
                            <th>기능/의의</th>
                            <th>주요 레퍼런스</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            </tr>
                            <tr>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            </tr>
                            <tr>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            </tr>
                            <tr>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            </tr>
                            <tr>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            </tr>
                            <tr>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            </tr>
                        </tbody>
                </table>

                    </div>
                    <div className="b-div"> <h4>상호작용 검토 결과</h4>
                        <table className='result-b'>
                        <thead>
                            <tr>
                            <th>유전자</th>
                            <th>SNP (변이)</th>
                            <th>유전형</th>
                            <th>관련 영양소</th>
                            <th>권장 영양제</th>
                            <th>기능/의의</th>
                            <th>주요 레퍼런스</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            </tr>
                        </tbody>
                </table>
                    </div>
                    
                </div>
            </div>
        </div>
        </div>
    )
}

export default Analyze;