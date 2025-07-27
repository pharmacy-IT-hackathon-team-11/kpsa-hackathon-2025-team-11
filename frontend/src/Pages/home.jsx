import { height } from '@fortawesome/free-brands-svg-icons/fa42Group';
import './home.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

// ✅ Article 컴포넌트
function Article({ image, title, detail }) {
    const navigate = useNavigate();
return (
    <div className='art' style={{ display: 'flex', marginBottom: '20px' }}>
    <div
        className="art-img"
        style={{
        width: '200px',
        height: '120px',
        backgroundImage: `url(${image})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        marginRight: '15px',
        borderRadius: '3px',
        flexShrink: 0
        }}
    ></div>
    <div className="art-text">
        <h2 className="art-title" style={{ fontSize: '18px', margin: 0 }}>{title}</h2>
        <span className="art-detail" style={{ fontSize: '14px', color: '#555' }}>{detail}</span>
    </div>
    </div>
);
}

// ✅ Home 컴포넌트
function Home() {
    console.log('로딩은 됐니?')
    const navigate = useNavigate();
    const [customerCount, setCustomerCount] = useState(null);

    // ✅ 예시: localStorage에서 token 불러옴
    const token = localStorage.getItem('token');

    useEffect(() => {
    async function getCount() {
        try {
        const res = await fetch('https://6mip5m9jtv.us-east-1.awsapprunner.com/api/v1/auth/my-customer-count', {
            method: 'GET',
            headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
            }
        });

        if (!res.ok) throw new Error(`고객 수 요청 실패 - 상태 코드: ${res.status}`);
        
        const data = await res.json();
        console.log('응답 데이터:', data);
        setCustomerCount(data.customer_count);
        } catch (err) {
        console.error('고객 수 가져오기 실패:', err);
        }
    }

    if (token) getCount();
    }, [token]);

    useEffect(() => {
    console.log('customerCount 변경됨:', customerCount);
    }, [customerCount]);


const articles = [
    {
    image: '/article/b1.jpg',
    title: '파스퇴르연구소, 숙명여대 약학연구소와 ‘노화 치료제’ 개발 나선다',
    detail: '한국파스퇴르연구소(소장 장승기, 이하 파스퇴르(연))는 지난 17일 숙명여자대학교 약학연구소(소장 장창영, 이하 숙명여대 약학연구소)와 노화·감염병 치료제 개발을 위한 연구 협약을 체결했다고 24일 밝혔다.',
    },
    {
    image: '/article/b2.jpg',
    title: '약대생, IT 창업 실현에 다가가다…약학xIT 창업 해커톤 개최',
    detail: '[메디파나뉴스 = 조해진 기자] 창업을 꿈꾸는 미래 약사들이 IT 개발자, 디자이너들과 머리를 맞대고 아이디어를 실현하기 위해 모였다.',
    },
    {
    image: '/article/b3.jpg',
    title: '약학정보원,“약물 유발성 갑상샘 기능 이상” 정보 제공',
    detail: '약학정보원(원장 유상준)은 7월 28일자 온라인 학술정보지 ‘팜리뷰’에 특정 약물로 인해 갑상샘에서 생성하는 호르몬의 양이 변하면서 발생하는 약물 유발성 갑상샘 기능 이상에 대해 다루었다.'
    },
    {
    image: '/article/b4.jpg',
    title: '민생쿠폰 효과 톡톡…폭염 뚫고 약국 앞 대기행렬',
    detail: '[데일리팜=강혜경 기자] 민생회복 지원금이 풀리면서 약국도 톡톡히 수혜를 누리고 있는 것으로 나타났다. 민생회복 지원금 신청·지급 첫 주부터 체감 효과가 나타나고 있는 것인데, 약국 역시 기대 이상이라는 평가가 나오고 있다. 처방약 결제는 물론 수요가 뜸해졌던 영양제 등까지 지갑이 열리고 있다는 것이다.',
    },
];

return (
    <div className='body'>
    <div className="upper">
        <div className='btn0'>
            <div><span className='q'>누적고객</span> <span className='an'>{customerCount}</span></div>
            <div><span className='q'>우리 약국 이용 고객</span > <span className='an'>{customerCount}</span></div>
            <div><span className='q'>전체 이용 고객</span> <span className='an'>{customerCount}</span></div>
        </div>
        <div className="btn1">
            <img src="/home/icon1.png" alt="" style={{height:'50px', marginBottom:'5px'}} />
            신규고객 접수하기</div>
        <div className="btn2" onClick={()=>navigate('/result')}>
            <img src="/home/icon2.png" alt="" style={{height:'50px', marginBottom:'5px'}} />
            분석지 보기</div>
        <div className="btn3">
            <img src="/home/icon3.png" alt="" style={{height:'50px', marginBottom:'5px'}} />
            메시지 보내기</div>
    </div>
    <div className="banner"></div>
    <div className="lower">
        <div className="side-banners">
        <div className="sb1"></div>
        <div className="sb2"></div>
        </div>
        <div className="articles">
        <h2 style={{ fontWeight: 'bold' }}>오늘의 소식</h2>
        <hr />
        {articles.map((item, idx) => (
            <Article
            key={idx}
            image={item.image}
            title={item.title}
            detail={item.detail}
            />
        ))}
        </div>
    </div>
    </div>
);
}


export default Home;