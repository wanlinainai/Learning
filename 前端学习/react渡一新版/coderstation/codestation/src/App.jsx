import './css/App.css';
import { Layout } from 'antd';
import PageFooter from './components/PageFooter';
import NavHeader from './components/NavHeader';
import RouteConfig from './router';
import LoginForm from './components/LoginForm';
import { useState } from 'react';
const { Header, Footer, Content } = Layout;

function App() {

  const [isModalOpen, setIsModalOpen] = useState(false);

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
        <RouteConfig></RouteConfig>
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
