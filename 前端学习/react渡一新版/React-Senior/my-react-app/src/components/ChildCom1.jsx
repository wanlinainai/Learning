function ChildCom1(props) {
  return (
    <div style={{
      width: '400px',
      height: '400px',
      backgroundColor: 'red'
    }} onMouseMove={props.mouseMoveHandle}>
      <h1>鼠标移动</h1>
      <p>当前鼠标的位置: x{props.points.x}  y{props.points.y}</p>
    </div>
  );
}

export default ChildCom1;