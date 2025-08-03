import { request } from '@umijs/max';
/**
 * 用户相关接口
 */

function getUserByPage(params) {
  return request('/api/user', {
    method: 'GET',
    params: {
      ...params
    }
  })
}

/**
 * 删除用户
 */
function deleteUser(userId) {
  return request(`/api/user/${userId}`, {
    method: 'delete'
  })
}

export default {
  getUserByPage,
  deleteUser
}
