import React from 'react';
import { Provider } from 'react-redux';
import Input from './components/Input';
import List from './components/List';
import "./css/App.css";

function App(props) {
  return (
    <Provider>
      <div className='container'>
        <h1 className='lead' style={{
          marginBottom: "30px"
        }}>待办事项</h1>
        <Input />
        <List />
      </div>
    </Provider>
  );
}

export default App;