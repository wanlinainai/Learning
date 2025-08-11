import React from 'react';
import { createPortal } from 'react-dom';
function Modal(props) {
  // 之前是直接返回的JSX。现在我们通过Portals指定JSX渲染的位置

  return createPortal((<div style={{
    width: '450px',
    height: '250px',
    border: '1px solid',
    position: 'absolute',
    left: 'calc(50% - 225px)',
    top: 'calc(50% - 125px)',
    textAlign: 'center',
    lineHeight: '250px'
  }}>
    模态框
  </div>), document.getElementById('modal'));
}

export default Modal;