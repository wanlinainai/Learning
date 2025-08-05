import { Button, Form, Image, Upload } from 'antd';
import React, { useRef } from 'react';
import { Input } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import TextArea from 'antd/lib/input/TextArea';

/**
 * 添加用户表单组件
 * @param {*} props 
 * @returns 
 */
function UserForm(props) {
  const { type, submitHandle, userInfo, setUserInfo } = props;
  const formRef = useRef();
  if (formRef.current) {
    formRef.current.setFieldsValue(userInfo);
  }

  /**
   * 更新用户信息
   */
  function updateInfo(newInfo, key) {
    const newUserInfo = { ...userInfo };
    if (typeof newInfo === 'string') {
      newUserInfo[key] = newInfo.trim();
    } else {
      newUserInfo[key] = newInfo;
    }
    setUserInfo(newUserInfo)
  }

  let avatarPreview = null;
  if (type === 'edit') {
    avatarPreview = (
      <Form.Item label="当前头像" name="avatarPreview">
        <Image src={userInfo?.avatar} width={100} />
      </Form.Item>
    )
  }

  return (
    <div>
      <Form
        name='basic'
        initialValues={userInfo}
        autoComplete='off'
        ref={formRef}
        onFinish={submitHandle}
      >
        <Form.Item label="登录账号" name="loginId" rules={
          [{ required: true, message: "登录账号不能是空" }]
        }>
          <Input placeholder="请输入用户名" value={userInfo?.loginId} onChange={(e) => updateInfo(e.target.value, 'loginId')} />
        </Form.Item>
        <Form.Item label="登录密码" name='loginPwd'>
          <Input.Password rows={6} placeholder='密码可选，默认是123456' value={userInfo?.loginPwd} onChange={(e) => updateInfo(e.target.value, 'loginPwd')} />
        </Form.Item>
        <Form.Item label="用户昵称" name='nickname'>
          <Input placeholder='昵称可选，默认是新用户' value={userInfo?.nickname} onChange={(e) => updateInfo(e.target.value, "nickname")} />
        </Form.Item>
        {avatarPreview}
        <Form.Item label="用户头像" valuePropName='fileList'>
          <Upload
            action='/api/upload'
            listType='picture-card'
            maxCount={1}
            onChange={(e) => {
              if (e.file.status === 'done') {
                const url = e.file.response.data;
                updateInfo(url, "avatar")
              }
            }}
          >
            <div>
              <PlusOutlined />
              <div
                style={{
                  marginTop: 8
                }}
              >头像可选</div>
            </div>
          </Upload>
        </Form.Item>
        <Form.Item label="用户邮箱" name='mail'>
          <Input value={userInfo?.mail} placeholder='选填' onChange={(e) => updateInfo(e.target.value, "mail")} />
        </Form.Item>

        <Form.Item label="QQ号码" name='qq'>
          <Input value={userInfo?.qq} placeholder='选填' onChange={(e) => updateInfo(e.target.value, "qq")} />
        </Form.Item>

        <Form.Item label="微信" name='wechat'>
          <Input
            value={userInfo?.wechat}
            placeholder="选填"
            onChange={(e) => updateInfo(e.target.value, 'wechat')}
          />
        </Form.Item>

        <Form.Item label="个人简介" name='intro'>
          <TextArea rows={6} value={userInfo?.intro} placeholder='选填' onChange={(e) => updateInfo(e.target.value, "intro")} />
        </Form.Item>

        <Form.Item>
          <Button type='primary' htmlType='submit'>
            {type === 'add' ? '添加' : '修改'}
          </Button>

          <Button type='link' htmlType='reset' className='resetBtn'>
            重置
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}

export default UserForm;