import { PlusOutlined } from '@ant-design/icons';
import { Button, Form, Image, Input, Radio, Upload } from 'antd';
import {useRef} from 'react';
import AdminController from '@/services/admin';

/**
 * 管理员表单
 * @param {*} props 
 * @returns 
 */
function AdminForm(props) {

  const formRef = useRef();
  const {type, submitHandle, adminInfo, setAdminInfo} = props;

  // 头像
  let avatarPreview = null;
  if(type === 'edit') {
    avatarPreview = (
      <Form.Item 
        label='当前头像'
        name="avatarPreview"
      >
        <Image src={adminInfo.avatar} width={100}/>
      </Form.Item>
    )
  }

  /**
   * 更新管理员信息
   * @param {*} newInfo 
   * @param {*} key 
   */
  function updateInfo(newInfo, key) {
    const newAdminInfo = {...adminInfo};
    if(typeof newInfo === 'string') {
      newAdminInfo[key] = newInfo.trim();
    } else {
      newAdminInfo[key] = newInfo;
    }
    setAdminInfo(newAdminInfo)
  }


  /**
   * 验证登录账号是否存在
   */
  async function checkLoginIdIsExist(_, value) {
    if (value && type === 'add') {
      const { data } = await AdminController.adminIsExist(value);
      if (data) {
        return Promise.reject(new Error('该管理员账号已经被注册'));
      }
    }
    return Promise.resolve();
  }


  return (
    <Form
      name='basic'
      initialValues={adminInfo}
      autoComplete='off'
      ref={formRef}
      onFinish={submitHandle}
      labelCol={{ span: 5 }}      // label 占 5 格
      wrapperCol={{ span: 12 }}   // 输入框占 12 格
    >
      <Form.Item
        label="管理员账号"
        name="loginId"
        rules={[
          {required: true, message: '请输入管理员账号'},
          // 验证用户是否已经存在
          {validator: checkLoginIdIsExist}
        ]}
        validateTrigger="onBlur" 
      >
        <Input 
          value={adminInfo?.loginId}
          onChange={(e) => updateInfo(e.target.value, 'loginId')}
          disabled = {type === 'edit' ? true : false}
        />
      </Form.Item>

      <Form.Item
        label="管理员密码"
        name="loginPwd"
        rules={[
          type === 'edit' ? {required: true, message: '密码不能为空'} : null
        ]}
      >
        <Input.Password
          placeholder='密码可选，默认是123123'
          value={adminInfo?.loginPwd}
          onChange={(e) => updateInfo(e.target.value, 'loginPwd')}
        />
      </Form.Item>

      <Form.Item
        label='管理员昵称'
        name='nickname'
      >
        <Input 
          placeholder='昵称可选，默认是新增管理员'
          value={adminInfo?.nickname}
          onChange={(e) => updateInfo(e.target.value, "nickname")}
        />
      </Form.Item>

      <Form.Item
        label="权限选择"
        name="permission"
        rules={[
          {required: true, message: '请选择管理员权限'}
        ]}
      >
        <Radio.Group>
          <Radio value={2}>普通管理员</Radio>
          <Radio value={1}>超级管理员</Radio>
        </Radio.Group>
      </Form.Item>

      {avatarPreview}
      <Form.Item
        label="上传头像"
        valuePropName='fileList'
      >
        <Upload
          action='/api/upload'
          listType='picture-card'
          maxCount={1}
          class="uploadStyle"
          onChange={(e) => {
            if(e.file.status === 'done') {
              // 上传已经完成
              const url = e.file.response.data;
              updateInfo(url, 'avatar');
            }
          }}
        >
          <div>
            <PlusOutlined/>
            <div 
              style={{
                marginTop: 8
              }}
            >头像可选</div>
          </div>
        </Upload>
      </Form.Item>

      {/* 按钮容器 */}
      <Form.Item
        wrapperCol={{offset: 5, span: 16}}
      >
        <Button 
          type='primary'
          htmlType='submit'
        >{type === 'add' ? '确认新增': "修改"}</Button>
        <Button type='link' htmlType='submit' className='resetBtn'>重置</Button>
      </Form.Item>
    </Form>
  );
}

export default AdminForm;