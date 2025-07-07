import React from "react";
import PropTypes from "prop-types";
class World extends React.Component {
  constructor(props) {
    super(props);
  }

  static defaultProps = {
    stuInfo: {
      name: '李白',
      age: 100
    }
  }
  render() {
    return (
      <>
        <ul>
          <li>姓名：{this.props.stuInfo.name}</li>
          <li>年龄：{this.props.stuInfo.age}</li>
          <li>content：{this.props.content}</li>
        </ul>
      </>
    );
  }
}

// props 默认值
// World.defaultProps = {
//   stuInfo: {
//     name: "李白",
//     age: 90
//   }
// }
World.propTypes = {
  content: PropTypes.string
}

// props 类型检测

export default World;