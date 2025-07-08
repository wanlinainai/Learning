import React from 'react'

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value1: "",
      value2: ""
    };
  }

  handleChange = (e) => {
    const name = e.target.name;
    switch (name) {
      case "one": {
        // 只能输入第一个输入框
        this.setState({
          value1: e.target.value.toUpperCase()
        })
        break;
      }
      case "two": {
        // 只能输入第二个输入框
        const newValue = e.target.value.split("").map(item => {
          if (!isNaN(item)) {
            return item
          }
        }).join("");
        this.setState({
          value2: newValue
        })
        break;
      }
    }
  }

  clickHandle = () => {
    console.log(`提交的内容是:${this.state.value}`);
  }

  render() {
    return (
      <div>
        <input type="text"
          name="one"
          value={this.state.value1}
          onChange={this.handleChange}
          placeholder='自动转成大写' />
        <input type="text"
          name='two'
          value={this.state.value2}
          onChange={this.handleChange}
          placeholder='只能输入数字' />
        <button onClick={this.clickHandle}>submit</button>
      </div>
    );
  }
}

export default App;