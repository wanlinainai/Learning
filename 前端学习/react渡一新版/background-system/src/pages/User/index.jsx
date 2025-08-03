import { lighten, PageContainer, ProTable } from '@ant-design/pro-components';
import { Button, Form, message, Popconfirm, Switch } from 'antd';
import { useState, useEffect, useRef } from 'react';
import UserController from '@/services/user';
import { useNavigate } from 'react-router-dom';
import { useAccess, Access } from 'umi';

function User(props) {

  const access = useAccess();
  const actionRef = useRef();

  const navigate = useNavigate();

  const columns = [
    {
      title: '序号',
      align: 'center',
      width: 50,
      search: false,
      render: (text, record, index) => {
        return [(pagination.current - 1) * pagination.pageSize + index + 1];
      }
    },
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
      align: 'center',
      search: false
    },
    {
      title: '昵称',
      dataIndex: 'nickname',
      key: 'nickname',
      align: 'center'
    },
    {
      title: '头像',
      dataIbndex: 'avatar',
      key: 'avatar',
      align: 'center',
      valueType: 'image',
      search: false
    },
    {
      title: '账号状态',
      dataIndex: 'enabled',
      key: 'enabled',
      align: 'center',
      search: false,
      render: (_, row, index, action) => {
        const defaultChecked = row.enabled ? true : false;
        return (
          <Switch
            key={row._id}
            defaultChecked={defaultChecked}
            size='small'
            onChange={(value) => switchChange(row, value)}
          />
        )
      }
    },
    {
      title: '操作',
      width: 200,
      key: 'option',
      valueType: 'option',
      fixed: 'right',
      align: 'center',
      render: (_, row, index, action) => {
        return [
          <div key={row._id}>
            <Button type='link' size='small' onClick={() => showModal()}>详情</Button>
            <Button type='link' size='small' onClick={() => navigate(`/user/editUser/${row._id}`)}>编辑</Button>
            {/* 加上删除确认认证 */}
            {/* <Access accessible={access.SuperAdmin}> */}
            <Popconfirm
              title="确认删除吗？"
              onConfirm={() => deleteHandle(row)}
              okText="删除"
              cancelText="取消"
            >
              <Button type='link' size='small'>删除</Button>
            </Popconfirm>
            {/* </Access> */}

          </div>
        ]
      }
    }
  ]

  /**
   * 删除用户
   * @param {*} userInfo 
   */
  function deleteHandle(userInfo) {
    UserController.deleteUser(userInfo._id);
    actionRef.current.reload();// 刷新请求
    message.success('删除用户成功')
  }

  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 5,
  })

  function handlePageChange(current, pageSize) {
    setPagination({
      current,
      pageSize
    })
  }

  return (
    <>
      <PageContainer>
        <ProTable
          headerTitle='用户列表'
          actionRef={actionRef}
          columns={columns}
          rowKey={(row) => row._id}
          pagination={{
            showQuickJumper: true,
            showSizeChanger: true,
            pageSizeOptions: [5, 10, 15, 20, 25, 30],
            ...pagination,
            onChange: handlePageChange,
          }}
          request={async (params) => {
            const result = await UserController.getUserByPage(params);
            return {
              data: result.data.data,
              success: !result.code,
              total: result.data.count
            }
          }}
        />
      </PageContainer>
    </>
  );
}

export default User;