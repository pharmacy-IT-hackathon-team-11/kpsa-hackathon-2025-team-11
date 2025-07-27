import { useState, useEffect } from 'react'


function Back(){
    const [message, setMessage] = useState('')
    const [message2, setMessage2] = useState('')
    const [message3, setMessage3] = useState('')

    useEffect(()=>{ //여기에서 사용한 then 문법은 promise:나중에 결과 준다는 것.
        fetch('https://6mip5m9jtv.us-east-1.awsapprunner.com/api/v1/auth/health') //fetch는 응답을 res 형태로 받는다.
        .then((res)=>res.json()) //json으로 바꾸기
        .then((data)=>{
        setMessage(data.status) //data를 받아서 message내용을 갱신한다.
        setMessage2(data.service)
        setMessage3(data.message)
        console.log(data)
        })
        .catch((err) => {
        console.error(err, '힝....ㅜㅜ')
        setMessage('죄송한데 못 받아왔셈 ;;;;')
        })
    }, []) //useeffect의 의존성 배열 -> 이펙트가 언제 실행될 지 결정한다.

    return(
        <div>
        <h3>health check</h3>
        <div className='msgbox' style={{border:'4px solid lightblue', padding:'20px', borderRadius:'10px', width:'300px'}}>
            <div>{message}
            <br />{message2}
            <br />{message3}
            </div>
        </div>
        </div>
    )
    }

export default Back;