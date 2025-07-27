import request from './request'

// 用户相关API

/**
 * 获取验证码
 */
export function getCaptcha() {
  return request({
    url: '/res/captcha',
    method: "get"
  })
}

/**
 * 查询用户是否存在
 */
export function userIsExist(loginId) {
  return request({
    url: `/api/user/exist/${loginId}`,
    method: "GET",
  });
}


/**
 * 用户注册
 */
export function addUser(newUserInfo) {
  return request({
    url: '/api/user',
    data: newUserInfo,
    method: "POST"
  })
}

/**
 * 用户登录
 */
export function userLogin(loginInfo) {
  return request({
    url: '/api/user/login',
    method: 'POST',
    data: loginInfo
  })
}

/**
 * 根据id查询用户
 */
export function getUserById(id) {
  return request({
    url: `/api/user/${id}`,
    method: 'GET'
  })
}

/**
 * 获取登录状态
 */
export function getInfo() {
  return request({
    url: '/api/user/whoami',
    method: 'GET'
  })
}

/**
 * 获取积分前十的用户
 */
export function getUserByPointsRank() {
  return request({
    url: '/api/user/pointsrank',
    method: 'GET'
  })
}

/**
 * 根据id修改用户
 */
export function editUser(userId, newUserInfo) {
  return request({
    url: `/api/user/${userId}`,
    method: 'patch',
    data: newUserInfo
  })
}

/**
 * 验证用户密码是否正确
 */
export function checkPassword(userId, loginPwd) {
  return request({
    url: "/api/user/passwordcheck",
    method: "post",
    data: {
      userId,
      loginPwd
    }
  })
}