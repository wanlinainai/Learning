import { Form, Modal, Radio, Input, Row, Col, Checkbox, Button, message } from 'antd';
import { useRef, useState, useEffect } from 'react';
import styles from '../css/LoginForm.module.css'
import { getCaptcha, userIsExist, addUser } from '../api/user';
import { initUserInfo, changeLoginStatus } from '../redux/userSlice';
import { useDispatch } from 'react-redux';

function LoginForm(props) {

  const [value, setValue] = useState(1)
  const [captcha, setCaptcha] = useState(null);
  const [messageApi, contextHolder] = message.useMessage();
  const loginFormRef = useRef();
  const registerFormRef = useRef();
  const dispatch = useDispatch();

  // 初始化时候调用
  useEffect(() => {
    captchaClickHandle()
  }, [props.isShow]);


  function loginHandle() {

  }
  function handleOk() {
  }

  function onChange(e) {
    // 修改value的值，达到单选框能够切换
    setValue(e.target.value)
    captchaClickHandle()
  }

  // 登录表单的状态数据
  const [loginInfo, setLoginInfo] = useState({
    loginId: '',
    loginPwd: '',
    capcha: "",
    remember: false
  })

  // 注册表单的状态数据
  const [registerInfo, setRegisterInfo] = useState({
    loginId: '',
    nickname: '',
    capcha: ''
  })

  let container = null;

  /**
   * 更新填入的数据
   * @param {*} oldInfo 
   * @param {*} newContent 
   * @param {*} key 
   * @param {*} setInfo 
   */
  function updateInfo(oldInfo, newContent, key, setInfo) {
    const obj = { ...oldInfo };
    obj[key] = newContent;
    setInfo(obj);
  }

  /**
   * 关闭弹框
   */
  function handleCancel() {
    // 清空上一次的内容
    setRegisterInfo({
      loginId: "",
      nickname: "",
      captcha: ''
    })

    setLoginInfo({
      loginId: "",
      loginPwd: '',
      captcha: '',
      remember: false
    })

    // 关闭
    props.closeModal();
  }

  /**
   * 注册点击事件
   */
  async function registerHandle() {
    const data = await addUser(registerInfo);
    if (data.data) {
      // 注册成功
      messageApi.open({
        type: 'success',
        content: '用户注册成功，默认密码是 123456'
      })
      // 用户信息存储到数据仓库中
      dispatch(initUserInfo(data.data))

      // 将数据仓库的登录状态修改
      dispatch(changeLoginStatus(true))

      // 关闭登录的弹框
      handleCancel()
    } else {
      // 失败
      messageApi.open({
        type: 'warning',
        content: data.msg,
      });

      captchaClickHandle();
    }

  }

  // 异步请求验证码接口
  async function captchaClickHandle() {
    const result = await getCaptcha();
    setCaptcha(result);
  }

  /**
   * 检查用户登录id是否存在
   */
  async function checkLoginIdIsExist() {
    if (registerInfo.loginId) {
      const { data } = await userIsExist(registerInfo.loginId)
      if (data) {
        return Promise.reject("该用户名已经被使用")
      }
    }
  }

  if (value === 1) {
    // 登录面板的jsx
    container = (
      <div className={styles.container}>
        {contextHolder}
        <Form
          name="basic1"
          autoComplete="off"
          onFinish={loginHandle}
          ref={loginFormRef}
        >
          <Form.Item
            label="登录账号"
            name="loginId"
            rules={[
              {
                required: true,
                message: "请输入账号",
              },
            ]}
          >
            <Input
              placeholder="请输入你的登录账号"
              value={loginInfo.loginId}
              onChange={(e) => updateInfo(loginInfo, e.target.value, 'loginId', setLoginInfo)}
            />
          </Form.Item>

          <Form.Item
            label="登录密码"
            name="loginPwd"
            rules={[
              {
                required: true,
                message: "请输入密码",
              },
            ]}
          >
            <Input.Password
              placeholder="请输入你的登录密码，新用户默认为123456"
              value={loginInfo.loginPwd}
              onChange={(e) => updateInfo(loginInfo, e.target.value, 'loginPwd', setLoginInfo)}
            />
          </Form.Item>

          {/* 验证码 */}
          <Form.Item
            name="logincaptcha"
            label="验证码"
            rules={[
              {
                required: true,
                message: '请输入验证码',
              },
            ]}
          >
            <Row align="middle">
              <Col span={16}>
                <Input
                  placeholder="请输入验证码"
                  value={loginInfo.captcha}
                  onChange={(e) => updateInfo(loginInfo, e.target.value, 'captcha', setLoginInfo)}
                />
              </Col>
              <Col span={6}>
                <div
                  className={styles.captchaImg}
                  onClick={captchaClickHandle}
                  dangerouslySetInnerHTML={{ __html: captcha }}
                ></div>
              </Col>
            </Row>
          </Form.Item>

          <Form.Item
            name="remember"
            wrapperCol={{
              offset: 5,
              span: 16,
            }}
          >
            <Checkbox
              onChange={(e) => updateInfo(loginInfo, e.target.checked, 'remember', setLoginInfo)}
              checked={loginInfo.remember}
            >记住我</Checkbox>
          </Form.Item>

          <Form.Item
            wrapperCol={{
              offset: 5,
              span: 16,
            }}
          >
            <Button
              type="primary"
              htmlType="submit"
              style={{ marginRight: 20 }}
            >
              登录
            </Button>
            <Button type="primary" htmlType="submit">
              重置
            </Button>
          </Form.Item>
        </Form>
      </div>
    )
  } else {
    // 注册面板的jsx
    container = (
      <div className={styles.container}>
        {contextHolder}
        <Form
          name="basic2"
          autoComplete="off"
          ref={registerFormRef}
          onFinish={registerHandle}
        >
          <Form.Item
            label="登录账号"
            name="loginId"
            rules={[
              {
                required: true,
                message: "请输入账号，仅此项为必填项",
              },
              // 验证用户是否已经存在
              { validator: checkLoginIdIsExist },
            ]}
            validateTrigger='onBlur'
          >
            <Input
              placeholder="请输入账号"
              value={registerInfo.loginId}
              onChange={(e) => updateInfo(registerInfo, e.target.value, 'loginId', setRegisterInfo)}
            />
          </Form.Item>

          <Form.Item
            label="用户昵称"
            name="nickname"
          >
            <Input
              placeholder="请输入昵称，不填写默认为新用户xxx"
              value={registerInfo.nickname}
              onChange={(e) => updateInfo(registerInfo, e.target.value, 'nickname', setRegisterInfo)}
            />
          </Form.Item>

          <Form.Item
            name="registercaptcha"
            label="验证码"
            rules={[
              {
                required: true,
                message: '请输入验证码',
              },
            ]}
          >
            <Row align="middle">
              <Col span={16}>
                <Input
                  placeholder="请输入验证码"
                  value={registerInfo.captcha}
                  onChange={(e) => updateInfo(registerInfo, e.target.value, 'captcha', setRegisterInfo)}
                />
              </Col>
              <Col span={6}>
                <div
                  className={styles.captchaImg}
                  onClick={captchaClickHandle}
                  dangerouslySetInnerHTML={{ __html: captcha }}
                ></div>
              </Col>
            </Row>
          </Form.Item>

          <Form.Item
            wrapperCol={{
              offset: 5,
              span: 16,
            }}
          >
            <Button
              type="primary"
              htmlType="submit"
              style={{ marginRight: 20 }}
            >
              注册
            </Button>
            <Button type="primary" htmlType="submit">
              重置
            </Button>
          </Form.Item>
        </Form>
      </div>
    )
  }
  return (
    <div>
      <Modal title="注册/登录" open={props.isShow} onOk={handleOk} onCancel={props.closeModal}>
        <Radio.Group
          value={value}
          onChange={onChange}
          className={styles.radioGroup}
          buttonStyle='solid'
        >
          <Radio.Button value={1} className={styles.radioButton}>登录</Radio.Button>
          <Radio.Button value={2} className={styles.radioButton}>注册</Radio.Button>
        </Radio.Group>

        {/* 需要显示对应功能的表单项 */}
        <div>
          {container}
        </div>
      </Modal>
    </div >
  );
}

export default LoginForm;