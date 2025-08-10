import React from 'react';
import ChildCom2 from './ChildCom2';
import ChildCom3 from './ChildCom3';

function ChildCom1() {
  return (
    <div>
      ChildCom1
      <ChildCom2 />
      <ChildCom3 />
    </div>
  );
}

export default ChildCom1;