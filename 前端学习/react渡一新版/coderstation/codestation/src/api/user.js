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