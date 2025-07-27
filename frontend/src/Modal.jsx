
import React, { useContext } from 'react';
import { ModalContext } from './ModalContext.jsx';

function Modal() {
  // '공구함'에서 '드라이버(closeModal)'만 정확히 꺼내옵니다.
  const { closeModal } = useContext(ModalContext);

  return (
    // 모달이 화면 전체를 덮도록 backdrop 스타일을 추가하는 것이 좋습니다.
    <div className="show modal" style={{ display: 'block' }}>
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">한 번 가입하면 이탈은 불가합니다</h5>
            <button
              type="button"
              className="btn-close"
              aria-label="Close"
              onClick={closeModal} // 닫기 함수 연결
            />
          </div>
          <div className="modal-body">
            <p>햄스터는 영원하다.</p>
          </div>
          <div className="modal-footer">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={closeModal} // 닫기 함수 연결
            >
              Close
            </button>
            <button type="button" className="btn btn-primary">
              Save changes
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Modal;
