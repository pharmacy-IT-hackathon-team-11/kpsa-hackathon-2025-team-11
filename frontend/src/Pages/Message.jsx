import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useContext } from 'react';
import { ModalContext } from '../ModalContext.jsx';
import './Message.css'

function Message() {
  const { closeMsg } = useContext(ModalContext);

  return (
    <div className="show right-modal" style={{ display: 'block', position:'absolute'}}>
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">
          <div className="modal-header" style={{padding:'20px'}}>
            <h5 className="modal-title">햄베르기우스 <span class="badge text-bg-success active" style={{borderRadius:'15px'}}>active</span></h5>
            <button
              type="button"
              className="btn-close"
              aria-label="Close"
              onClick={closeMsg}
            />
          </div>
          <div className="msgbody">
          </div>
          <div className="modal-footer">
            <textarea name="" id=""></textarea>
            <button
              type="button"
              className="btn btn-secondary"
            >
              전송
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Message;
