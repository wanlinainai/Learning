import React from "react";
import Hello from './component/Hello'
import World from "./component/World";
import Button from "./component/Button";
import Greeting from "./component/Greeting";

// function App() {
//   const name = "litaibai";
//   const test = "three";
//   const styles = {
//     color: 'green',
//     fontSize: '50px'
//   }

//   // const arr = [
//   //   (<div>这是div数组元素</div>)
//   //     (<span>这是span数组元素</span>)
//   //     (<p>这是p数组元素</p>)
//   // ]

//   const stuInfo = [
//     { id: 1, name: "李白", age: 20 },
//     { id: 2, name: "李逵", age: 20 },
//     { id: 3, name: "李大白", age: 20 },
//   ]
//   const arr2 = stuInfo.map(item => {
//     return (
//       <div key={item.id}>姓名：{item.name} 年龄：{item.age}</div>
//     )
//   })

//   const element1 = <h1 className="greeting">Hello world</h1>
//   // React.createElement()函数：1. HTML或者组件名 2. 属性 3. 子元素

//   const element2 = React.createElement(
//     'h1',
//     { className: 'greeting' },
//     "Hello world"
//   )
//   const ele = (<>
//     <ul>
//       <li id="one">1</li>
//       <li id="two">2</li>
//       <li id={test}>{name === 'litaibai' ? "李太白" : null}</li>
//     </ul>

//     <ul style={styles} className="aa">
//       <li id="one">1</li>
//       <li id="two">2</li>
//       <li id={test}>{name === 'litaibai' ? "李太白2" : null}</li>
//     </ul>
//     {/* {arr} */}
//     {arr2}
//     {element1}
//     {element2}
//   </>
//   )

//   function clickHandle(e) {
//     console.log(e)
//     console.log(e.nativeEvent) // 原生事件对象
//   }

//   function eventHandler(str, e) {
//     e.preventDefault();
//     console.log(str);
//   }

//   const ele2 = (
//     <>
//       <button onClick={clickHandle}>
//         按钮
//       </button>

//       <a href="https://www.baidu.com" onClick={(e) => eventHandler("参数param", e)}>redirect Baidu</a>
//     </>
//   )

//   const ele3 = (
//     <div>Hello</div>
//   )
//   return ele3;
// }

// 类组件
//  this的修正只针对于类组件
class App extends React.Component {
  // 1 constructor use state
  constructor() {
    super()
    // this.clickHandle = this.clickHandle.bind(this);
    // this.state = {
    //   num: 1
    // }

    // this.timer = setInterval(() => {
    //   this.setState({
    //     num: this.state.num + 1
    //   })

    //   console.log(this.state.num, 'num');
    // }, 1000);
  }

  state = {
    name: 'zhangdebiao',
    age: 19
  }

  // state = {
  //   num: 12
  // }
  // Function 1 : () => {}
  // clickHandle = () => {
  //   // alert("hello")
  //   console.log(this)
  // }

  // Function 2 : 在JSX中使用箭头函数（事件绑定的时候）
  // clickHandle() {
  //   alert('Hello')
  // }

  // Function 3 : bind()
  // clickHandle() {
  //   console.log(this)
  // }

  // clickHandle = () => {
  // this.state.num++  ----> Wrong . Use setState() function to 
  // const newNum = this.state.num + 1;
  // this.setState({
  //   num: this.state.num + 1
  // }, () => {
  //   console.log(this.state.num, 'num')
  // })
  // this.setState((pre) => ({
  //   num: pre.num + 1
  // }))
  // this.setState((pre) => ({
  //   num: pre.num + 1
  // }))
  // }

  // 传递给子组件
  changeStateHandle(number) {
    console.log('子组件传递过来的数据', number);
  }
  render() {
    return (
      // this.clickHandle方法定位到类属性方法
      // <div onClick={this.clickHandle}>点击事件</div>
      // <div onClick={() => this.clickHandle()}>点击事件</div>
      <>
        {/* {this.state.num}
        <button onClick={this.clickHandle}>+1</button> */}
        <Hello stuInfo={this.state} num={false} changeStateHandle={this.changeStateHandle} />
        <World content="content内容" />
        <Button>添加按钮</Button>

        {/* 条件渲染 --> 是否登录 */}
        <Greeting isLoggedIn={true}/>
      </>
    )
  }
}

export default App;