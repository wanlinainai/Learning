import { lighten, PageContainer, ProTable } from '@ant-design/pro-components';
import { Button, Form, message, Modal, Popconfirm, Switch, Tag } from 'antd';
import { useState, useEffect, useRef } from 'react';
import UserController from '@/services/user';
import { useNavigate } from 'react-router-dom';
import { useAccess, Access } from 'umi';
import { formatDate } from '@/utils/tools';

function User(props) {

  const access = useAccess();
  const actionRef = useRef();

  const [userInfo, setUserInfo] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

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
            <Button type='link' size='small' onClick={() => showModal(row)}>详情</Button>
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
   * 状态切换
   */
  function switchChange(row, value) {
    UserController.editUser(row._id, {
      enabled: value
    });

    if (value) {
      message.success('用户状态已经激活')
    } else {
      message.success('该用户已禁用')
    }
  }

  /**
   * 显示编辑的内容
   */
  function showModal(row) {
    setIsModalOpen(true)
    setUserInfo(row);
  }

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
  const handleCancel = () => {
    setIsModalOpen(false);
  };
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

      <Modal title={userInfo?.nickname} open={isModalOpen} onCancel={handleCancel} footer={null} style={{ top: 20 }}>
        <h3>登录账号</h3>
        <p>
          <Tag color='red'>{userInfo?.loginId}</Tag>
        </p>
        <h3>登录密码</h3>
        <p>
          <Tag color='magenta'>{userInfo?.loginPwd}</Tag>
        </p>
        <h3>联系方式</h3>
        <div
          style={{
            display: 'flex',
            width: '350px',
            justifyContent: 'space-between'
          }}
        >
          <div>
            <h4>QQ</h4>
            <p>{userInfo?.qq ? userInfo.qq : "未填写"}</p>
          </div>
          <div>
            <h4>微信</h4>
            <p>{userInfo?.wechat ? userInfo.wechat : '未填写'}</p>
          </div>
          <div>
            <h4>邮箱</h4>
            <p>{userInfo?.mail ? userInfo.mail : '未填写'}</p>
          </div>
        </div>

        <h3>个人简介</h3>
        <p>{userInfo?.intro ? userInfo.intro : "未填写"}</p>

        <h3>时间信息</h3>
        <div
          style={{
            display: 'flex',
            width: '450px',
            justifyContent: 'space-between'
          }}
        >
          <div>
            <h4>注册时间</h4>
            <p>{formatDate(userInfo?.registerDate)}</p>
          </div>

          <div>
            <h4>上次登录</h4>
            <p>{formatDate(userInfo?.lastLoginDate)}</p>
          </div>
        </div>

        <h3>当前积分</h3>
        <p>{userInfo?.points}</p>
      </Modal>
    </>
  );
}

export default User;