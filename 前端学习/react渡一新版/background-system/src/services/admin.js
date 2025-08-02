import { request } from '@umijs/max';

/**
 * 获取所有管理员
 */
function getAdmin() {
  return request('/api/admin', {
    method: 'GET'
  })
}

/**
 * 检查账户是否存在
 * @param {*} loginId 
 * @returns 
 */
function adminIsExist(loginId) {
  return request(`/api/admin/adminIsExist/${loginId}`, {
    method: "GET"
  })
}

/**
 * 新增管理员
 */
function addAdmin(newAdminInfo) {
  return request('/api/admin', {
    method: 'post',
    data: newAdminInfo
  })
}

export default {
  getAdmin,
  adminIsExist,
  addAdmin
}