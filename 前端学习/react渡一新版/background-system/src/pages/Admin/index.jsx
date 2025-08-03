import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'umi';
import {
  PageContainer,
  ProTable,
} from '@ant-design/pro-components';
import { Switch, Tag, Space, Button, Popconfirm, message, Modal } from 'antd';
import AdminForm from './components/adminForm';
function Admin(props) {
  const dispatch = useDispatch();

  const { adminList } = useSelector(state => state.admin);

  // 控制弹窗开关
  const [isModalOpen, setIsModalOpen] = useState(false);

  // 保存当前登录用户
  const [adminInfo, setAdminInfo] = useState(null);


  useEffect(() => {
    dispatch({
      type: 'admin/_initAdminList'
    })
  }, [adminList]);



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
      align: 'center',
      valueType: 'image'
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
    {
      title: '账号状态',
      dataIndex: 'enabled',
      key: "enabled",
      align: 'center',
      render: (_, row) => {
        return (
          <Switch
            key={row._id}
            size='small'
            defaultChecked={row.enabled ? true : false}
            onChange={(value) => switchChange(row, value)}
          />
        )
      }
    },
    {
      title: '操作',
      width: 150,
      key: "option",
      align: 'center',
      render: (_, row) => {
        return (
          <Space key={row._id}>
            <Button type="link" size="small" onClick={() => showModal(row)}>编辑</Button>
            <Popconfirm
              title="确定删除吗?"
              onConfirm={() => deleteHandle(row)}
              okText="Yes"
              cancelText="No"
            >
              <Button type="link" size="small">删除</Button>
            </Popconfirm>

          </Space>
        )
      }
    }
  ]

  /**
   * 打开修改弹出框面板
   * @param {*} row 
   */
  function showModal(row) {
    setAdminInfo(row);
    setIsModalOpen(true);
  }

  /**
   * 点击OK按钮
   */
  const handleOk = () => {
    dispatch({
      type: 'admin/_editAdmin',
      payload: {
        adminInfo,
        newAdminInfo: adminInfo
      }
    })

    setIsModalOpen(false);
    message.success('修改成功');
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  /**
   * 修改管理员状态
   * @param {*} adminInfo 
   * @param {*} checked 
   */
  function switchChange(row, value) {
    dispatch({
      type: 'admin/_editAdmin',
      payload: {
        adminInfo: row,
        newAdminInfo: {
          enabled: value
        }
      }
    })

    value ? message.success('管理员已激活') : message.success('管理员已禁用')
  }

  /**
   * 删除管理员
   * @param {*} adminInfo 
   */
  function deleteHandle(adminInfo) {
    // 需要判断是否是当前登录的用户
    // 派发Action
    dispatch({
      type: 'admin/_deleteAdmin',
      payload: adminInfo
    })
    message.success('删除成功')
  }

  return (
    <div>
      <PageContainer>
        <ProTable
          headerTitle='管理员列表'
          dataSource={adminList}
          rowKey={(row) => row._id}
          columns={columns}
          search={false}
          pagination={{
            pageSize: 5
          }}
        />
      </PageContainer>

      <Modal title="修改信息"
        open={isModalOpen}
        onOk={handleOk}
        onCancel={handleCancel}
        footer={null}>
        <AdminForm
          type='edit'
          submitHandle={handleOk}
          adminInfo={adminInfo}
          setAdminInfo={setAdminInfo}
        />
      </Modal>
    </div>
  );
}

export default Admin;