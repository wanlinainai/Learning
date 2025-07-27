import React, { useState } from 'react';
import PageHeader from '../components/PageHeader';
import styles from '../css/Personal.module.css';
import { useSelector } from 'react-redux';
import { Card, Image, Upload, Modal, Form, Input, Button, message } from 'antd';
import PersonalInfoItem from '../components/PersonalInfoItem';
import { formatDate } from '../utils/tools';
import { PlusOutlined } from '@ant-design/icons';
import { updateUserInfoAsync } from '../redux/userSlice';
import { useDispatch } from 'react-redux';
import { checkPassword } from '../api/user';

/**
 * 个人中心
 * @param {*} props 
 * @returns 
 */
function Personal(props) {

  const { userInfo } = useSelector(state => state.user);
  const dispatch = useDispatch();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [panelName, setPanelName] = useState("");
  const [passwordInfo, setPasswodInfo] = useState({
    oldpassword: "", // 旧密码
    newpassword: "", // 新密码
    passwordConfirm: "", // 验证密码
  })
  const [editInfo, setEditInfo] = useState({}); // 编辑的用户信息

  const showModal = (name) => {
    setPanelName(name)
    // 清空上一次的内容
    setEditInfo({});
    setIsModalOpen(true);
  };

  const handleOk = () => {
    // setIsModalOpen(false);
    dispatch(updateUserInfoAsync({
      userId: userInfo._id,
      newInfo: editInfo
    }));
    message.success('更新信息成功')
    setIsModalOpen(false)
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  function handleAvatar(newURL, key) {
    // 将仓库和服务器端的数据一并更新
    dispatch(updateUserInfoAsync({
      userId: userInfo._id,
      newInfo: {
        [key]: newURL
      }
    }))
  }

  // 更新密码信息
  function updatePasswordInfo(newInfo, key) {
    const newPasswordInfo = { ...passwordInfo };
    newPasswordInfo[key] = newInfo.trim();
    setPasswodInfo(newPasswordInfo);
  }

  /**
   * 检查密码是否正确
   */
  async function checkPasswordIsRight() {
    if (passwordInfo.oldpassword) {
      const { data } = await checkPassword(userInfo._id, passwordInfo.oldpassword);
      console.log(data)
      if (!data) {
        // 密码不正确
        return Promise.reject('密码错误')
      }
    }
  }

  /**
   * 更新用户信息
   */
  function updateInfo(newInfo, key) {
    if (key === 'nickname' && !newInfo) {
      message.error("昵称不能为空")
      return;
    }
    const newUserInfo = { ...editInfo };
    newUserInfo[key] = newInfo;
    setEditInfo(newUserInfo);
  }

  // 模态框中间显示的内容
  let modalContent = null;
  switch (panelName) {
    case "基本信息": {
      modalContent = (
        <>
          <Form
            name='basic1'
            autoComplete='off'
            onFinish={handleOk}
            initialValues={userInfo}
          >
            {/* 登录密码 */}
            <Form.Item
              label="登录密码"
              name="oldpassword"
              rules={[
                { validator: checkPasswordIsRight },
                { required: true }
              ]}
              validateTrigger='onBlur'
            >
              <Input.Password
                rows={6}
                value={passwordInfo.oldpassword}
                placeholder='如果要修改密码，请先输入旧密码'
                onChange={(e) => updatePasswordInfo(e.target.value, "oldpassword")}
              />
            </Form.Item>

            {/* 新的登录密码 */}
            <Form.Item
              label="新密码"
              name="newpassword"
            >
              <Input.Password
                rows={6}
                value={passwordInfo.newpassword}
                placeholder='请输入新密码'
                onChange={(e) => updatePasswordInfo(e.target.value, "newpassword")}
                rules={[
                  { required: true }
                ]}
              />
            </Form.Item>

            {/* 确认密码 */}
            <Form.Item
              label="确认密码"
              name="passwordConfirm"
              // 校验两次输入的密码是否相同
              rules={[
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue('newpassword') === value) {
                      return Promise.resolve();
                    }
                    return Promise.reject(new Error('两次输入的密码不一致'));
                  },
                }),
                {
                  required: true
                }
              ]}
              validateTrigger="onBlur"
            >
              <Input.Password
                rows={6}
                value={passwordInfo.passwordConfirm}
                placeholder='请确认密码'
                onChange={(e) => updatePasswordInfo(e.target.value, "passwordConfirm")}
              />
            </Form.Item>

            {/* 用户昵称 */}
            <Form.Item
              label="用户昵称"
              name="nickname"
            >
              <Input
                placeholder='昵称可选，默认为新用户'
                value={userInfo.nickname}
                onBlur={(e) => { updateInfo(e.target.value, "nickname") }} />
            </Form.Item>

            {/* 确认修改按钮 */}
            <Form.Item wrapperCol={{ offset: 5, span: 16 }} style={{}}>
              <Button
                type='primary'
                htmlType='submit'
              >确认
              </Button>
              <Button
                type='link'
                htmlType='reset'
                className="resetBtn"
              >重置</Button>
            </Form.Item>
          </Form>
        </>
      )
      break;
    }
    case "社交账号": {
      modalContent = (
        <>
          <Form name='basic2'
            initialValues={userInfo}
            autoComplete='off'
            onFinish={handleOk}
          >
            <Form.Item
              name="mail"
              label="邮箱"
            >
              <Input
                value={userInfo.mail}
                placeholder='请填写邮箱'
                onChange={(e) => updateInfo(e.target.value, "mail")}
              />
            </Form.Item>

            <Form.Item
              name="qq"
              label="QQ号"
            >
              <Input
                value={userInfo.qq}
                placeholder='请填写QQ号'
                onChange={(e) => updateInfo(e.target.value, "qq")}
              />
            </Form.Item>

            <Form.Item
              name="wechat"
              label="微信"
            >
              <Input
                value={userInfo.wechat}
                placeholder='请填写微信号'
                onChange={(e) => updateInfo(e.target.value, "wechat")}
              />
            </Form.Item>
            <Form.Item
              name="github"
              label="github"
            >
              <Input
                value={userInfo.github}
                placeholder='请填写github'
                onChange={(e) => updateInfo(e.target.value, "github")}
              />
            </Form.Item>

            {/* 按钮 */}
            <Form.Item wrapperCol={{ offset: 5, span: 16 }}>
              <Button
                type='primary'
                htmlType='submit'>
                确认
              </Button>

              <Button type='link' htmlType='reset' className='resetBtn'>
                重置
              </Button>
            </Form.Item>
          </Form>
        </>
      )
      break;
    }
    case "个人简介": {
      modalContent = (
        <>
          <Form
            name='basic3'
            initialValues={userInfo}
            autoComplete='off'
            onFinish={handleOk}
          >
            {/* 自我介绍 */}
            <Form.Item
              label="自我介绍"
              name="intro"
            >
              <Input.TextArea
                rows={6}
                value={userInfo.intro}
                placeholder='选填'
                onChange={(e) => updateInfo(e.target.value, 'intro')}
              />
            </Form.Item>

            <Form.Item wrapperCol={{ offset: 5, span: 16 }}>
              <Button type='primary' htmlType='submit'>
                确认
              </Button>

              <Button type='link' htmlType='reset' className="resetBtn">
                重置
              </Button>
            </Form.Item>
          </Form>
        </>
      )
      break;
    }
  }

  return (
    <div>
      <PageHeader title="个人中心" />
      {/* 信息展示 */}
      <div className={styles.container}>
        {/* 基本信息 */}
        <div className={styles.row}>
          <Card title="基本信息" extra={(<div className={styles.edit} onClick={() => showModal("基本信息")}>编辑</div>)}>
            <PersonalInfoItem info={{ itemName: "登录账号", itemValue: userInfo.loginId }} />
            <PersonalInfoItem info={{ itemName: "账号密码", itemValue: '**** **** ***' }} />
            <PersonalInfoItem info={{ itemName: "用户昵称", itemValue: userInfo.nickname }} />
            <PersonalInfoItem info={{ itemName: "用户积分", itemValue: userInfo.points }} />
            <PersonalInfoItem info={{ itemName: "注册时间", itemValue: formatDate(userInfo.registerDate) }} />
            <PersonalInfoItem info={{ itemName: "上次登录时间", itemValue: formatDate(userInfo.lastLoginDate) }} />
            <div style={{ fontWeight: '100', height: "50px" }}>当前头像</div>
            <Image src={userInfo.avatar} width={100} />
            <div style={{ fontWeight: '100', height: "50px" }}>上传新头像</div>
            <Upload
              action='/api/upload'
              maxCount={1}
              listType='picture-card'
              onChange={(e) => {
                if (e.file.status === 'done') {
                  // 上传完成
                  const url = e.file.response.data;
                  // 处理用户头像更新
                  handleAvatar(url, 'avatar');
                }
              }}
            >
              <PlusOutlined />
            </Upload>
          </Card>
        </div>
        {/* 社交账号 */}
        <div className={styles.row}>
          <Card title="社交账号" extra={(<div className={styles.edit} onClick={() => showModal("社交账号")}>编辑</div>)}>
            <PersonalInfoItem info={{ itemName: "邮箱", itemValue: userInfo.mail ? userInfo.mail : "未填写" }} />
            <PersonalInfoItem info={{ itemName: "QQ号", itemValue: userInfo.qq ? userInfo.qq : "未填写" }} />
            <PersonalInfoItem info={{ itemName: "微信号", itemValue: userInfo.wechat ? userInfo.wechat : "未填写" }} />
            <PersonalInfoItem info={{ itemName: "Github", itemValue: userInfo.github ? userInfo.github : "未填写" }} />
          </Card>
        </div>
        {/* 个人简介 */}
        <div className={styles.row}>
          <Card title="个人简介" extra={(<div className={styles.edit} onClick={() => showModal("个人简介")}>编辑</div>)}>
            <p className={styles.intro}>
              {userInfo.intro ? userInfo.intro : "未填写"}
            </p>
          </Card>
        </div>
      </div>

      {/* 修改信息的对话框 */}
      <Modal title={panelName} open={isModalOpen} onOk={handleOk} onCancel={handleCancel} footer={false}>
        {modalContent}
      </Modal>
    </div>
  );
}

export default Personal;