import React, { useEffect, useRef, useState } from 'react';

function App(props) {

    const [counter, setCounter] = useState(1);

    // 使用 useRef 来保存定时器的 id
    let timer = useRef(null);

    useEffect(() => {
        timer.current = setInterval(() => {
            console.log('触发了');
        }, 1000)
    }, [])

    const clearTimer = () => {
        clearInterval(timer.current)
    }

    // 点击 +1
    function clickHandle() {
        console.log(timer)
        setCounter(counter + 1);
    }
    return (
        <div>
            <div>{counter}</div>
            <button onClick={clickHandle}>+1</button>
            <button onClick={clearTimer}>停止</button>
        </div>
    );
}

export default App;