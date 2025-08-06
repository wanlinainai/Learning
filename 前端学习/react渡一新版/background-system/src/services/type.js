import { request } from 'umi';

/**
 * 获取类型列表
 * @returns 
 */
function getType() {
  return request('/api/type', {
    method: 'GET'
  })
}

/**
 * 新增类型
 * @param {*} newTypeInfo 
 */
function addType(newTypeInfo) {
  return request('/api/type', {
    method: 'POST',
    data: newTypeInfo
  })
}

export default {
  getType,
  addType
}