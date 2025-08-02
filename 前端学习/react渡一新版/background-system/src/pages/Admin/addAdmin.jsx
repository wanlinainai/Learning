import { PageContainer } from '@ant-design/pro-components';
import React, { useEffect, useState } from 'react';
import AdminForm from '../Admin/components/adminForm';
import { useDispatch, useSelector } from '@umijs/max';
import { useNavigate } from '@umijs/max';
import { message } from 'antd';

function AddAdmin(props) {

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const {adminList} = useSelector(state => state.admin);

  const [newAdminInfo, setNewAdminInfo] = useState({
    loginId: '',
    loginPwd: '',
    nickname: '',
    avatar: "",
    permission: 2
  })

  useEffect(() => {
    if(!adminList.length) {
      dispatch({
        type: 'admin/_initAdminList'
      })
    }
  }, [adminList])

  // 用户点击新增按钮
  function submitHandle() {
    if(newAdminInfo.loginId) {
      dispatch({type: 'admin/_addAdmin', payload: newAdminInfo});
      message.success('添加管理员成功')
      // 跳转回首页
      navigate('/admin/adminList');
    }
  }

  return (
    <PageContainer>
      <div className='container' style={{width: 500}}>
        <AdminForm 
          type="add"
          submitHandle={submitHandle}
          adminInfo = {newAdminInfo}
          setAdminInfo = {setNewAdminInfo}
        />
      </div>
      
    </PageContainer>
  );
}

export default AddAdmin;