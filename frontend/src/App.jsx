import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import { Helmet } from 'react-helmet';
import { useNavigate } from 'react-router-dom';
import { useEffect, useRef } from 'react';



// Pricing 컴포넌트는 App.jsx 안에 두거나 별도 파일로 분리할 수 있습니다.
function Pricing() {
  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-md-8 col-lg-6">
          <div className="card shadow-lg">
            <div className="card-body p-5">
              <h2 className="card-title text-center mb-4">햄스터들은 늘 배고픕니다</h2>
              <p className="card-text text-center mb-4">
                프리미엄 서비스 필요하면 결제해라.<br />
                결제 완료 후, 모든 기능을 무제한으로 이용하실 수 있습니다.<br />
                안전한 결제 시스템을 통해 빠르고 간편하게 결제하실 수 있습니다.
              </p>
              <ul className="list-group list-group-flush mb-4">
                <li className="list-group-item">✔️ 톱밥 제거</li>
                <li className="list-group-item">✔️ 실시간 지원</li>
                <li className="list-group-item">✔️ 프리미엄 댄스 기능 제공</li>
              </ul>
              <div className="d-grid gap-2">
                <button className="btn btn-primary btn-lg" disabled>
                  결제하기 (준비중)
                </button>
              </div>
              <div className="alert alert-info mt-4" role="alert">
                현재는 결제 시스템이 준비 중입니다.<br />
                곧 다양한 결제 수단(카드, 계좌이체, 간편결제 등)이 지원될 예정입니다.<br />
                문의: <a href="mailto:support@example.com">support@example.com</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function Footer(){
  return(
    <footer>
      <span>이메일: nananaba1@snu.ac.kr </span>
      <span>Copyright 2025. hamstersekai. All rights reserved.</span>
      <span>always remember HAMSTER AROUND U</span>
    </footer>
  )
}

function App({isLoggedin, handleLoginSuccess}) {
  const navigate = useNavigate();
  if (isLoggedin){
    console.log('로그인 됐어!')
  }else{
    console.log('로그인 안 됐어')
  }

  return (
    <>
      <Helmet>
        <title>DNAble</title>
      </Helmet>
      <Page1 />
      <Page2 />
      <Page3 />
      <Page4 />
      <Page5 />
    </>
  )
}

function Page1(){
  return(
    <>
    <div className="a">
      <div className="a-title">
        유전자 기반 AI 분석 리포트, <br />
        약사가 완성하는 맞춤형 건강 상담
      </div>
      <span className='a-text'>유전자 검사 결과에 따라 필요한 영양소를 AI가 제안하고 약사가 검토하여 최종 상담합니다.</span>
      <button className='btn btn-outline-primary a-button' style={{borderRadius:'20px', border: '1px solid white', color:'white'}}>서비스 시작하기 &gt;</button>
    </div>
    </>
  )
}

function Page2(){
  return(
    <>
    <div className="b">
      <h1 className='b-title'>우리의 서비스는?</h1>
      <span className='b-detail'>About our Services</span>
      <div className="b-box">
        <div className="box1">
          <img src="/main/main6-1.png" style={{height:'50px', marginBottom:'20px'
          }} alt="" />
          유전자 검사 키트 연동</div>
        <div className="box2">
          <img src="/main/main6-2.png" style={{height:'50px', marginBottom:'20px'
          }} alt="" />
          AI 분석 기반 영양소 추천</div>
        <div className="box3">
          <img src="/main/main6-3.png" style={{height:'50px', marginBottom:'20px'
          }} alt="" />약사가 직접 상담 및 최종 추천</div>
        <div className="box4">
          <img src="/main/main6-4.png" style={{height:'50px', marginBottom:'20px'
          }} alt="" />고객 건강 데이터 기반 관리</div>
      </div>
      <span style={{margin:'50px'}}>약국의 전문성을 강화하고, 단골 고객 만족도를 높이는 헬스케어 솔루션입니다.</span>
    </div>
    </>
  )
}

function Page3(){
  return(
    <>
    <div className="c">
      <div className="c-title">약사에게는 직능확장을<br />
      소비자에게는 올바른 영양제를 <br />
      사회적으로는 약물 오남용 방지를<br />
      <span style={{fontWeight:'100', fontSize:'20px'}}>your journey with us</span></div>
      <div className="c-1"><span className="num">01</span><p>고객 정보 입력 및</p><p>바코드 생성</p></div>
      <div className="c-2"><span className="num">02</span><p>검사기관 수령 후</p><p>검사기관 전달</p></div>
      <div className="c-3"><span className="num">03</span><p>AI 분석 완료 후</p><p>약국 시스템 자동 반영</p></div>
    </div>
    </>
  )
}

function Page4() {
  const pointsRef = useRef([]);

  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('show');
        }
      });
    }, { threshold: 0.3 });

    pointsRef.current.forEach(point => {
      if (point) observer.observe(point);
    });

    return () => {
      pointsRef.current.forEach(point => {
        if (point) observer.unobserve(point);
      });
    };
  }, []);

  const pointItems = [
    {
      title: "유전자 리스크 요약",
      text: "예: 혈당 대사 저하, 비타민 D 대사 문제 등"
    },
    {
      title: "AI 기반 필요한 영양소 자동 추천",
      text: "철분, 오메가 3 등 부족 분석"
    },
    {
      title: "중복 복용 여부 분석, 상담 리포트 생성",
      text: "예: 규칙적인 수면, 운동 권장 등"
    },
    {
      title: "생활 습관에 맞춘 맞춤 추천 제공",
      text: "약사의 검토 후 제공되는 상담 리포트"
    }
  ];

  return (
    <div className="d">
      <div className="d-1"></div>
      <div className="d-2">
        <div className="d-title">AI가 추천한 결과를 <br /> 어떻게 보나요?</div>
        <div className="points">
          {pointItems.map((item, i) => (
            <div
              className="point"
              key={i}
              ref={el => pointsRef.current[i] = el}
            >
              <div className="point-title">{item.title}</div>
              <div className="point-text">{item.text}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function Page5() {
  const boxRefs = useRef([]);
  const navigate = useNavigate();

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('show');
          }
        });
      },
      { threshold: 0.2 }
    );

    boxRefs.current.forEach((box) => {
      if (box) observer.observe(box);
    });

    return () => {
      boxRefs.current.forEach((box) => {
        if (box) observer.unobserve(box);
      });
    };
  }, []);

  const benefits = [
    {
      icon: "/main/main5-1.png",
      texts: ["검사 키트 공급", "정산 시스템 제공"]
    },
    {
      icon: "/main/main5-2.png",
      texts: ["상담 리포트 축적", "고객관리 기능"]
    },
    {
      icon: "/main/main5-3.png",
      texts: ["고객 만족도 상승으로", "단골 유치"]
    },
    {
      icon: "/main/main5-4.png",
      texts: ["초기 셋업 무료 지원", "(교육자료 제공)"]
    }
  ];

  return (
    <div className="b">
      <h1 className="b-title">파트너 약국이 되면?</h1>
      <div className="e-box" style={{ display: 'flex', flexWrap: 'wrap', gap: '20px', justifyContent: 'center' }}>
        {benefits.map((item, i) => (
          <div
            key={i}
            ref={(el) => (boxRefs.current[i] = el)}
            className={`flip-in`}
            style={{
              transitionDelay: `${i * 0.3}s`,
              background: '#f8f9fa',
              padding: '20px',
              borderRadius: '12px',
              width: '220px',
              boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
              textAlign: 'center'
            }}
          >
            {item.icon && (
              <img
                src={item.icon}
                alt=""
                style={{ height: "80px", marginTop:'30px', marginBottom: "30px" }}
              />
            )}
            {item.texts.map((text, j) => (
              <p key={j}>{text}</p>
            ))}
          </div>
        ))}
      </div>
      <button
        className="btn btn-success bu-ton"
        style={{
          borderRadius: "50px",
          width: "300px",
          height: "40px",
          marginTop: "50px",
          backgroundColor:'rgba(46, 107, 193, 0.826)'
        }}
        onClick={() => navigate('/login')}
      >
        지금 시작하기
      </button>
    </div>
  );
}
export default App;