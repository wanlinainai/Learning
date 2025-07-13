import logo from './logo.svg';
import './css/App.css';
import { Layout } from 'antd';
import PageFooter from './components/PageFooter';
import NavHeader from './components/NavHeader';

const { Header, Footer, Content } = Layout;

function App() {
  return (
    <div className="App">
      {/* 头部 */}
      <Header>
        <NavHeader />
      </Header>
      {/* 内容 */}
      <Content>
        这是内容哈哈哈
      </Content>
      {/* 底部 */}
      <Footer className='footer'>
        <PageFooter />
      </Footer>
    </div>
  );
}

export default App;
