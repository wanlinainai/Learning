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

/**
 * 删除管理员
 */
function deleteAdmin(adminId) {
  return request(`/api/admin/${adminId}`, {
    method: 'delete'
  })
}

/**
 * 更新管理员信息
 * @param {*} adminId 
 * @param {*} newAdminInfo 
 */
function editAdmin(adminId, newAdminInfo) {
  return request(`/api/admin/${adminId}`, {
    method: 'patch',
    data: newAdminInfo
  })
}

export default {
  getAdmin,
  adminIsExist,
  addAdmin,
  deleteAdmin,
  editAdmin
}