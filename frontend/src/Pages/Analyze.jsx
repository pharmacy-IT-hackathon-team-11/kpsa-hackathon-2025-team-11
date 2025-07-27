import './Analyze.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useState, useEffect } from 'react'

function Analyze(){
    const [customers, setCustomers] = useState([]);
    const [selectedCustomer, setSelectedCustomer] = useState(null);
    const [geneAnalysis, setGeneAnalysis] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const API_BASE_URL = 'https://6mip5m9jtv.us-east-1.awsapprunner.com/api/v1/auth';

    // 고객 목록 불러오기
    useEffect(() => {
        const fetchCustomers = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    setError('로그인이 필요합니다.');
                    return;
                }

                const response = await fetch(`${API_BASE_URL}/customers/`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });

                if (!response.ok) {
                    throw new Error('고객 목록을 불러오는데 실패했습니다.');
                }

                const data = await response.json();
                setCustomers(data.customers || []);
            } catch (err) {
                console.error('Error fetching customers:', err);
                setError(err.message);
            }
        };

        fetchCustomers();
    }, []); // 의존성 배열이 비어있음 - 컴포넌트 마운트 시에만 실행

    // 고객 상세 정보 불러오기
    const fetchCustomerDetails = async (customerId) => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`${API_BASE_URL}/customers/${customerId}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('고객 정보를 불러오는데 실패했습니다.');
            }

            // 현재는 selectedCustomer에 이미 필요한 정보가 있어서 사용하지 않음
            // const data = await response.json();
        } catch (err) {
            console.error('Error fetching customer details:', err);
            setError(err.message);
        }
    };

    // 유전자 분석 결과 불러오기
    const fetchGeneAnalysis = async (customerId) => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`${API_BASE_URL}/gene-analysis/customers/${customerId}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('유전자 분석 결과를 불러오는데 실패했습니다.');
            }

            const data = await response.json();
            setGeneAnalysis(data);
        } catch (err) {
            console.error('Error fetching gene analysis:', err);
            setError(err.message);
        }
    };

    // 고객 선택 처리
    const handleCustomerSelect = (e) => {
        const customerId = e.target.value;
        const customer = customers.find(c => c.id === customerId);
        setSelectedCustomer(customer);
        if (customer) {
            fetchCustomerDetails(customerId);
        }
    };

    // 결과 보기 버튼 클릭
    const handleShowResults = async () => {
        if (!selectedCustomer) {
            setError('고객을 선택해주세요.');
            return;
        }

        setLoading(true);
        setError('');
        
        try {
            await fetchGeneAnalysis(selectedCustomer.id);
        } finally {
            setLoading(false);
        }
    };

    return(
        <div className="fullbody">
        
        <div className='analyze-body'>
            <h1>분석 결과</h1>
            {error && <div style={{color: 'red', textAlign: 'center', marginBottom: '10px'}}>{error}</div>}
            <div className="containers">
                <div className="left">
                    <form onSubmit={(e) => e.preventDefault()}>
                        <label>고객 선택
                            <select onChange={handleCustomerSelect} value={selectedCustomer?.id || ''}>
                                <option value="">고객을 선택하세요</option>
                                {customers.map(customer => (
                                    <option key={customer.id} value={customer.id}>
                                        {customer.full_name} ({customer.birth_date})
                                    </option>
                                ))}
                            </select>
                        </label>
                        {selectedCustomer && (
                            <>
                                <label>이름<input type="text" value={selectedCustomer.full_name} readOnly /></label>
                                <label>생년월일<input type="text" value={selectedCustomer.birth_date} readOnly /></label>
                                <label>연락처<input type="tel" value={selectedCustomer.phone_number} readOnly /></label>
                                <label>유전자 킷 상태<input type="text" value={selectedCustomer.gene_kit_status} readOnly /></label>
                                <label>현재 복용 중인 약물 및 기저질환<textarea value={selectedCustomer.description || ''} readOnly></textarea></label>
                            </>
                        )}
                    </form>
                <button type="button" onClick={handleShowResults} disabled={!selectedCustomer || loading}>
                    {loading ? '분석 중...' : '결과보기'}
                </button>
                </div>
                <div className="right">
                    <div className="a-div"><h4>{geneAnalysis ? `${geneAnalysis.customer_name}님 검사 결과` : '검사 결과'}</h4>
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
                            {geneAnalysis?.analysis_results && geneAnalysis.analysis_results.length > 0 ? 
                                geneAnalysis.analysis_results.map((result, index) => (
                                    <tr key={`gene-${result.gene}-${result.snp}-${index}`}>
                                        <td>{result.gene}</td>
                                        <td>{result.snp}</td>
                                        <td>{result.customer_representation}</td>
                                        <td>{result.related_nutrition || 'N/A'}</td>
                                        <td>-</td>
                                        <td>{result.related_feature || 'N/A'}</td>
                                        <td>{result.pmid || 'N/A'}</td>
                                    </tr>
                                )) :
                                <tr>
                                    <td colSpan="7">분석 결과를 불러오려면 고객을 선택하고 '결과보기'를 클릭하세요.</td>
                                </tr>
                            }
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
                            {geneAnalysis?.analysis_results ? 
                                geneAnalysis.analysis_results
                                    .filter(result => result.match_status === 'exact_match')
                                    .length > 0 ?
                                    geneAnalysis.analysis_results
                                        .filter(result => result.match_status === 'exact_match')
                                        .map((result, index) => (
                                            <tr key={`match-${result.gene}-${result.snp}-${index}`}>
                                                <td>{result.gene}</td>
                                                <td>{result.snp}</td>
                                                <td>{result.customer_representation}</td>
                                                <td>{result.related_nutrition || 'N/A'}</td>
                                                <td>-</td>
                                                <td>{result.related_feature || 'N/A'}</td>
                                                <td>{result.pmid || 'N/A'}</td>
                                            </tr>
                                        )) :
                                    <tr>
                                        <td colSpan="7">완전 일치하는 상호작용 결과가 없습니다</td>
                                    </tr>
                                :
                                <tr>
                                    <td colSpan="7">분석 결과가 없습니다</td>
                                </tr>
                            }
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