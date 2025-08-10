## React 高级

### Ref

包含以下内容：

- 过时API：String类型的Refs
- createRefAPI
- Ref转发
- useRef与useImperativeHandle

#### 过时API：String类型的Refs

```react
export default class App extends Component {
  clickHandle = () => {
    console.log(this);
    console.log(this.refs);
    this.refs.inputRef.focus();
  }
  
  render() {
    return (
    	<div>
      	<input type="text" ref="inputRef"/>
        <button onClick={this.clickHandle}>聚焦</button>
      </div>
    )
  }
}
```

#### useRef 和 useImperativeHandle

##### useRef 和 createRef

虽然useRef和createRef都是创建Ref的，但是还是有一些区别。主要体现在以下方面：

- useRef是hooks的一种，一般用于function组件，而createRef一般用于class组件。
- 由useRef创建的Ref对象在组件的整个生命周期内都不会改变，但是由于createRef创建的ref对象，组件每更新一次，Ref对象都会被重新创建。

正是由于createRef的创建Ref的弊端，组件每次都会更新，出现了useRef Hooks函数来解决这个问题。

useRef还接受一个初始值，用在关联DOM元素中没有卵用，但是在作为存储不需要变化的全局变量中非常方便。

