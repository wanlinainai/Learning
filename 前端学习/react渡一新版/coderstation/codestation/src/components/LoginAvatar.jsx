import { useSelector } from 'react-redux';
import { Avatar, Button, List, Popover,Image } from 'antd';
import styles from "../css/LoginAvatar.module.css";
import { UserOutlined } from '@ant-design/icons';
import { clearUserInfo, changeLoginStatus } from '../redux/userSlice';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';

// 组件用于显示用户头像，如果没有登录显示注册登录
function LoginAvatar(props) {
  const { isLogin, userInfo } = useSelector(state => state.user);

  const dispatch = useDispatch();
  const navigate = useNavigate();

  function listClickHandle(item) {
    if(item === '个人中心') {

    } else {
      // 退出登录
      // 清除Token
      localStorage.removeItem("userToken")
      // 清除状态仓库
      dispatch(clearUserInfo)
      dispatch(changeLoginStatus(false))
      navigate('/')
    }
  }

  let loginStatus = null;
  if (isLogin) {
    const content = (
      <List
        dataSource={["个人中心", "退出登录"]}
        size='large'
        renderItem={(item) => {
          return (
            <List.Item style={{ cursor: 'pointer' }} onClick={() => listClickHandle(item)}>{item}</List.Item>
          )
        }}
      >
      </List>
    )
    loginStatus = (
      <Popover content={content} trigger="hover" placement='bottom'>
        <div className={styles.avatarContainer}> 
          <Avatar src={<Image src={userInfo?.avatar} preview={false}/>} size='large' icon={<UserOutlined />} />
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