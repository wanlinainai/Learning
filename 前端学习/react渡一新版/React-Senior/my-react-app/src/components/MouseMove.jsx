import React, { useState } from 'react';

function MouseMove(props) {
  const [points, setPoints] = useState({
    x: 0,
    y: 0
  })

  function mouseMoveHandle(e) {
    setPoints({
      x: e.clientX,
      y: e.clientY
    })
  }

  return (
    props.render ? props.render({ points, mouseMoveHandle }) : null
  );
}

export default MouseMove;