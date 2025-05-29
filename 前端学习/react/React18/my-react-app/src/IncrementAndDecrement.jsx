import { useState } from "react"

function IncrementAndDecrement() {
  const [count, setCount] = useState(0)
  function incre() {
    setCount(prev => prev + 1)
    setCount(prev => prev + 1)
    setCount(prev => prev + 1)
  }

  function reset() {
    setCount(0)
  }

  function decre() {
    setCount(prev => prev - 1)
    setCount(prev => prev - 1)
    setCount(prev => prev - 1)
    setCount(prev => prev - 1)
  }
  return (
    <>
      <h1>Count: {count}</h1>
      <button onClick={incre}>Increment</button>
      <button onClick={reset}>Reset</button>
      <button onClick={decre}>Decrement</button>
    </>
  )
}

export default IncrementAndDecrement


// 如果在setCount的时候没有使用prev => prev + 1的形式，那么由于React的更新是异步操作的，不会直接更新count，所以拿到的都是0，最终就是 + 1的结果。
// 同时由于React在设置多个相同值的时候会进行合并，来优化性能