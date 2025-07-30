import { useEffect } from 'react';
import { useDispatch, useSelector } from 'umi';
import {
  PageContainer,
  ProTable,
} from '@ant-design/pro-components';
import { Tag } from 'antd';
function Admin(props) {
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch({
      type: 'admin/_initAdminList'
    })
  }, []);

  const { adminList } = useSelector(state => state.admin);

  const columns = [
    {
      title: '登录账号',
      dataIndex: 'loginId',
      key: 'loginId',
      align: 'center'
    },
    {
      title: '登录密码',
      dataIndex: 'loginPwd',
      key: 'loginPwd',
      align: 'center'
    },
    {
      title: '昵称',
      dataIndex: 'nickname',
      key: 'nickname',
      align: 'center'
    },
    {
      title: '头像',
      dataIndex: 'avatar',
      key: 'avatar',
      align: 'center'
    },
    {
      title: '权限',
      dataIndex: 'permission',
      key: 'permission',
      align: 'center',
      render: (_, row) => {
        let tag = row.permission === 1 ? <Tag color="red" key={row._id}>管理员</Tag> : <Tag color="orange" key={row._id}>普通用户</Tag>
        return tag
      }
    },
  ]

  return (
    <div>
      <PageContainer>
        <ProTable
          headerTitle='管理员列表'
          dataSource={adminList}
          rowKey={(row) => row._id}
          columns={columns}
        />
      </PageContainer>
    </div>
  );
}

export default Admin;