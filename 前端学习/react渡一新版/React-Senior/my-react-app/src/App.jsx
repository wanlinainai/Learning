import { useState } from 'react';
import Modal from './components/Modal';

function App(props) {

  const [isShow, setIsShow] = useState(false);


  return (
    <div id='root'>
      <div style={{
        position: 'relative',
      }}>
        <h1>App组件</h1>
        <button onClick={() => setIsShow(!isShow)}>显示/隐藏</button>
        {isShow ? <Modal /> : null}
      </div>

      <div id='modal'></div>
    </div>

  );
}

export default App;