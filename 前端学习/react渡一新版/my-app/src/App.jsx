import React from "react";
class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
    // create a ref，回头我们就可以获取到和该Ref绑定的DOM节点
    this.inputCon = React.createRef();
  }

  clickHandle = () => {
    console.log(this.inputCon.current.value)
  }

  render() {
    return (
      <div>
        <input type="text" ref={this.inputCon} />
        <button onClick={this.clickHandle}>获取用户输入内容</button>
      </div>
    );
  }
}

export default App;