function Button() {
  let count = 0;

  // const handleClick = (name) => {
  //   if (count < 3) {
  //     count++;
  //     console.log(`${name} you clicked me ${count} times/s`)
  //   } else {
  //     console.log(`${name} stop clicking me!`)
  //   }
  // }

  const handleClick = (e) => e.target.textContent = 'OUCH!👐🏼'

  // const handleClick2 = (name) => {
  //   console.log(`${name} stop click me `);
  // }
  // 使用回调函数可以大幅简化代码的编写
  return (
    <button onDoubleClick={(e) => handleClick(e)}>
      Click me 
    </button>
  )
}

export default Button