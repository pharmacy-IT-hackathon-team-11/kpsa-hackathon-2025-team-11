//모달에 대한 정보를 방송할 모달 방송국입니다!
import React, { createContext, useState } from 'react';

export const ModalContext = createContext();

export function ModalProvider({ children }) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isMsgOpen, setIsMsgOpen] = useState(false);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  const openMsg = () => setIsMsgOpen(true);
  const closeMsg = () => setIsMsgOpen(false);

  const value = {
    isModalOpen,
    openModal,
    closeModal,
    isMsgOpen,
    openMsg,
    closeMsg,
  };

  return <ModalContext.Provider value={value}>{children}</ModalContext.Provider>;
}