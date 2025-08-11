function ChildCom2(props) {
  return (
    <div style={{
      width: '400px',
      height: '400px',
      backgroundColor: 'grey',
      position: 'relative',
      overflow: 'hidden'
    }}
      onMouseMove={props.mouseMoveHandle}
    >
      <h1>移动鼠标</h1>
      <div style={{
        width: '15px',
        height: '15px',
        borderRadius: '50%',
        backgroundColor: 'black',
        position: 'absolute',
        left: props.points.x - 5 - 450,
        top: props.points.y - 5 - 12
      }}>

      </div>
    </div>
  );
}

export default ChildCom2;