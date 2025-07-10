// 封装请求函数

import request from "./request";

/**
 * 获取学生列表
 * @returns 
 */
export function getStuListApi() {
  return request({
    url: '/students',
    method: "GET"
  })
}

/**
 * 添加学生
 */
export function addStuApi(data) {
  return request({
    url: '/students',
    method: 'post',
    data
  })
}

/**
 * 根据id获取信息
 */
export function getStuByIdApi(id) {
  return request({
    url: `/students/${id}`,
    method: 'GET'
  })
}

/**
 * 根据id删除用户
 * @param  id 
 */
export function deleteStuById(id) {
  return request({
    url: `/students/${id}`,
    method: 'DELETE'
  })
}

/**
 * 根据id修改用户信息
 * @param {*} id 
 */
export function editStuById(id, data) {
  return request({
    url: `/students/${id}`,
    method: 'patch',
    data: data
  })
}