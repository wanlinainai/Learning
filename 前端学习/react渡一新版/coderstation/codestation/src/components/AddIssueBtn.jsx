import React from 'react';
import { Button, message } from 'antd';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';

/**
 * 添加问答
 */
function AddIssue(props) {

  const { isLogin } = useSelector(state => state.user)
  const navigate = useNavigate();

  function clickHandle() {
    // 跳转到问答页面，校验登录
    if (isLogin) {
      // 跳转
      navigate("/addIssue")
    } else {
      // 请先登录
      message.error('登录过期，请重新登录')
    }
  }
  return (
    <div>
      <Button type='primary'
        size='large'
        style={{
          width: "100%",
          marginBottom: "30px"
        }}
        onClick={clickHandle}
      >我要发问</Button>
    </div>
  );
}

export default AddIssue;