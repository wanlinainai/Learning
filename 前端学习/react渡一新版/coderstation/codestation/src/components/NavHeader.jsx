import React from 'react';
import { NavLink } from 'react-router-dom';

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
    </div>
  );
}

export default NavHeader;