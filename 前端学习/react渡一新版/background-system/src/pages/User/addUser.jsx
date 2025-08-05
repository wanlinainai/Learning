import { PageContainer } from '@ant-design/pro-components';
import React, { useState } from 'react';
import UserForm from './components/userForm';
import { useNavigate } from '@umijs/max';
import { message } from 'antd';
import UserController from '@/services/user';

function AddUser(props) {

  const navigate = useNavigate();

  const [newUserInfo, setNewUserInfo] = useState({
    loginId: '',
    loginPwd: '',
    avatar: '',
    nickname: '',
    mail: '',
    qq: '',
    wechat: '',
    intro: ''
  })

  const submitHandle = () => {
    UserController.addUser(newUserInfo);

    navigate('/user/userList');
    message.success('添加用户成功');
  };

  return (
    <PageContainer>
      <div className='container' style={{ width: 800 }}>
        <UserForm
          type="add"
          submitHandle={submitHandle}
          userInfo={newUserInfo}
          setUserInfo={setNewUserInfo}
        />
      </div>
    </PageContainer>
  );
}

export default AddUser;