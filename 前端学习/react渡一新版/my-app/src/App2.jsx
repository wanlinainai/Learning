import React from "react";
import Money from "./component/Money";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      doller: "",
      rmb: ""
    };
  }

  // toRmb
  transformToRmb = (value) => {
    console.log(value)
    if (parseFloat(value) || value === "" || parseFloat(value) === 0) {
      this.setState({
        doller: value,
        rmb: value === "" ? "" : (value * 7.5).toFixed(2)
      })
    } else {
      alert("Please input a number ")
    }
  }

  // toDoller
  transformToDoller = (value) => {
    if (parseFloat(value) || value === '' || parseFloat(value) === 0) {
      this.setState({
        doller: value === "" ? "" : (value * 0.35).toFixed(2),
        rmb: value
      })
    } else {
      alert("Please input a number")
    }
  }
  render() {
    return (
      <div>
        <Money text="美元" money={this.state.doller} transform={this.transformToRmb} />
        <Money text="人民币" money={this.state.rmb} transform={this.transformToDoller} />
      </div>
    );
  }
}

export default App;