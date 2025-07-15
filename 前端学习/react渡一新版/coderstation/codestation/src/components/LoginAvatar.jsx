import React from 'react';
import { useSelector } from 'react-redux';
import { Avatar, Button, List, Popover } from 'antd';
import styles from "../css/LoginAvatar.module.css";
import { UserOutlined } from '@ant-design/icons';

// 组件用于显示用户头像，如果没有登录显示注册登录
function LoginAvatar(props) {
  const { isLogin } = useSelector(state => state.user);

  let loginStatus = null;
  if (isLogin) {
    const content = (
      <List
        dataSource={["个人中心", "退出登录"]}
        size='large'
        renderItem={(item) => {
          return (
            <List.Item style={{ cursor: 'pointer' }}>{item}</List.Item>
          )
        }}
      >
      </List>
    )
    loginStatus = (
      <Popover content={content} trigger="hover" placement='bottom'>
        <div className={styles.avatarContainer}>
          <Avatar src="" preview={false} size='large' icon={<UserOutlined />} />
        </div>
      </Popover>
    )
  } else {
    loginStatus = (
      <Button type="primary" size="large" onClick={props.loginHandle}>注册/登录</Button>
    )
  }
  return (
    <div>
      {loginStatus}
    </div>
  );
}

export default LoginAvatar;