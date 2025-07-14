import React from 'react';
import { NavLink } from 'react-router-dom';
import { Input, Select } from 'antd';
import LoginAvatar from './LoginAvatar';

function NavHeader(props) {
  return (
    <div className='headerContainer'>
      {/* 头部 logo */}
      <div className='logoContainer'>
        <div className='logo'></div>
      </div>
      {/* 头部导航 */}
      <nav className='navContainer'>
        <NavLink to="/" className="navigation">问答</NavLink>
        <NavLink to="/books" className="navigation">书籍</NavLink>
        <NavLink to="/interviews" className="navigation">面试题</NavLink>
        <a
          href="https://www.baidu.com"
          className='navigation'
          target='_blank'
        >视频教程</a>
      </nav>
      {/* 搜索框 */}
      <div className="searchContainer">
        <Select defaultValue="issue" size='large'
          style={{ width: '20%', borderTopRightRadius: 0, borderBottomRightRadius: 0 }}
          bordered={true}
        >
          <Select.Option value="issue">问答</Select.Option>
          <Select.Option value="book">书籍</Select.Option>
        </Select>
        <Input.Search
          placeholder='请输入搜索内容'
          allowClear
          enterButton="搜索"
          size='large'
          style={{
            width: "80%",
            borderTopLeftRadius: 0,
            borderBottomLeftRadius: 0
          }}
        />
      </div>

      {/* 登录按钮 */}
      <div className="loginBtnContainer">
        {/* 自定义头像组件 */}
        <LoginAvatar loginHandle={props.loginHandle} />
      </div>
    </div>
  );
}

export default NavHeader;