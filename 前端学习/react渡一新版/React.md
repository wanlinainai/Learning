# React 18.2.0

## Hooks

### 基本介绍

> Hook是React16.8新增特性，可以在不编写class的情况下使用state以及其他的React特性。

Hooks的出现，解决了如下的一些问题：

- 告别生命周期

> 以下代码中相同的代码实现了两遍。componentDidMount和componentDidUpdate

```react
import React from 'react'

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
      count: 0
     };
  }

  componentDidMount() {
    document.title =  `You clicked ${this.state.count} times`
  }

  componentDidUpdate() {
    document.title = `You clicked ${this.state.count} times`
  }

  render() {
    return (
      <div>
        <p>You clicke {this.state.count} times</p>
        <button onClick={() => {this.setState({count: this.state.count + 1})}}>
          Click me
        </button>
      </div>
    );
  }
}

export default App;
```

- 告别class中的this

> 在类组件中，存在this的指向问题，比如在事件处理函数中，不能直接通过this获取组件实例，需要修改this指向。

- 告别繁重的类组件，回归到函数

> 用类组件的话需要继承React.Component。会存在许多多余的冗余内容。

Hooks的出现就整个React思想上的转变，从“面向对象”到“函数式编程”。在学习Hooks的时候，会发现突然多了很多不熟悉的概念，`纯函数`、`副作用`、`柯里化`、`高阶函数`等概念。



Hook就是JavaScript函数，但是使用的话会有两个额外的规则：

- 只能在`函数最外层`调用Hook。不能在循环、条件判断或者子函数中使用。
- 只能在React的函数组件中调用Hook，不要在其他JavaScript函数中调用。

### useState和useEffect

React内置了一些实用的Hook，并且随着React版本的更新，Hook的数量还在持续的增加。

















