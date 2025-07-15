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