import React from 'react'

function Hello(props) {

  function clickHandle() {
    props.changeStateHandle(10086);
  }
  return (
    <>
      <ul>
        <li>姓名：{props.stuInfo.name}</li>
        <li>年龄：{props.stuInfo.age}</li>
        <li>content：{props.content}</li>
        <li>num：{props.num ? "true" : "false"}</li>
      </ul>

      <button onClick={clickHandle}>触发父组件传递过来的函数</button>

    </>
  )
}

// 设置 Hello 默认值
Hello.defaultProps = {
  content: 1000
}

export default Hello;