import React from "react";

function App() {
  const name = "litaibai";
  const test = "three";
  const styles = {
    color: 'green',
    fontSize: '50px'
  }

  // const arr = [
  //   (<div>这是div数组元素</div>)
  //     (<span>这是span数组元素</span>)
  //     (<p>这是p数组元素</p>)
  // ]

  const stuInfo = [
    { id: 1, name: "李白", age: 20 },
    { id: 2, name: "李逵", age: 20 },
    { id: 3, name: "李大白", age: 20 },
  ]
  const arr2 = stuInfo.map(item => {
    return (
      <div key={item.id}>姓名：{item.name} 年龄：{item.age}</div>
    )
  })

  const element1 = <h1 className="greeting">Hello world</h1>
  // React.createElement()函数：1. HTML或者组件名 2. 属性 3. 子元素
  
  const element2 = React.createElement(
    'h1',
    { className: 'greeting' },
    "Hello world"
  )
  return (
    <>
      <ul>
        <li id="one">1</li>
        <li id="two">2</li>
        <li id={test}>{name === 'litaibai' ? "李太白" : null}</li>
      </ul>

      <ul style={styles} className="aa">
        <li id="one">1</li>
        <li id="two">2</li>
        <li id={test}>{name === 'litaibai' ? "李太白2" : null}</li>
      </ul>
      {/* {arr} */}
      {arr2}
      {element1}
      {element2}
    </>
  );
}

export default App;
