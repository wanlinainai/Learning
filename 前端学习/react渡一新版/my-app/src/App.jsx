import {React, useState, useEffect} from 'react';
import useMyBook from './useMyBook';

function App() {

  const {bookName, setBookName} = useMyBook();
  const [value, setValue] = useState("");

  // 初始值, set初始值
  // let [count, setCount] = useState(0);
  // let [count1, setCount1] = useState(0);
  // let [count2, setCount2] = useState(0);
  // let [count3, setCount3] = useState(0);

  // useEffect(() => {
  //   // document.title = `你点击了${count}次`
  //   // const stopTimer = setInterval(() => {
  //   //   console.log("Hello");
  //   // }, 1000);

  //   console.log('副作用函数执行了....');
    
  //   // 在这个useEffect中，返回一个函数，该函数就是清理函数
  //   // return () => {
  //   //   // console.log('清理函数执行了');
  //   //   clearInterval(stopTimer)
  //   // }


  // }, []);

  // 使用多变量
  // let [age, setAge] = useState(42);
  // const [fruit, setFruit] = useState('banana');
  // const [todos, setTodos] = useState([{ text: '学习 Hook' }]);

  // function clickHandle() {
  //   // setCount(++count);
  //   // setAge(++age);
  //   // console.log('执行副作用函数');
    
  // }
  

  function changeHandle(e) {
    setValue(e.target.value);
  }

  function clickHandle() {
    setBookName(value)
  }

  return (
    <div>
      {/* <div>count1：{count1}</div>
      <div>count2：{count2}</div>
      <div>count3：{count3}</div> */}
      {/* <div>You clicked {count} times</div> */}
      {/* <div>年龄：{age}</div>
      <div>水果：{fruit}</div>
      <div>计划：{todos[0].text}</div> */}
      {/* <button onClick={clickHandle}>+ 1</button> */}
      {/* <button onClick={() => {setCount1(++count1)}}>+1</button>
      <button onClick={() => {setCount2(++count2)}}>+1</button>
      <button onClick={() => {setCount3(++count3)}}>+1</button> */}

        <div>{bookName}</div>
        <input type="text" value={value} onChange={changeHandle}/>
        <button onClick={clickHandle}>确定</button>
    </div>
  );
}

export default App;