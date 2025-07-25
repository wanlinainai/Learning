import './css/App.css';
import { Layout, message } from 'antd';
import PageFooter from './components/PageFooter';
import NavHeader from './components/NavHeader';
import RouteConfig from './router';
import LoginForm from './components/LoginForm';
import { useState, useEffect } from 'react';
import { getInfo, getUserById } from './api/user';
import { changeLoginStatus, initUserInfo } from './redux/userSlice';
import { useDispatch } from 'react-redux';
import RouteBefore from './router/RouteBefore';

const { Header, Footer, Content } = Layout;

function App() {

  const [isModalOpen, setIsModalOpen] = useState(false);

  const dispatch = useDispatch();

  // 加载根组件的时候需要恢复用户的登录状态
  useEffect(() => {
    async function fetchData() {
      const result = await getInfo()
      // token是过期还是成功
      if (result.data) {
        const { data } = await getUserById(result.data._id);
        dispatch(initUserInfo(data));
        dispatch(changeLoginStatus(true));
      } else {
        // 过期了，删除token 
        localStorage.removeItem('userToken')
        // 弹出提醒
        message.warning('登录过期，请重新登录')
      }

    }

    if (localStorage.getItem("userToken")) {
      fetchData();
    }
  })

  //关闭弹窗
  function closeModal() {
    setIsModalOpen(false);
  }

  // 打开弹框
  function loginHandle() {
    setIsModalOpen(true);

  }
  return (
    <div className="App">
      {/* 头部 */}
      <Header>
        <NavHeader loginHandle={loginHandle} />
      </Header>
      {/* 内容 */}
      <Content className='content'>
        <RouteBefore />
      </Content>
      {/* 底部 */}
      <Footer className='footer'>
        <PageFooter />
      </Footer>
      {/* 登录弹窗 */}
      <LoginForm isShow={isModalOpen} closeModal={closeModal} />
    </div>
  );
}

export default App;
