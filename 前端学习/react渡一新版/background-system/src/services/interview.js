import { request } from '@umijs/max';

/**
 * 新增面试题
 */
function addInterview(newInterviewInfo) {
  return request('/api/interview', {
    method: 'post',
    data: newInterviewInfo
  })
}

/**
 * 获取面试题表格页面
 */
function getInterviewByPage(params) {
  return request('/api/interview', {
    method: 'GET',
    params: {
      ...params
    }
  })
}

/**
 * 删除面试题
 */
function deleteInterview(id) {
  return request(`/api/interview/${id}`, {
    method: 'delete'
  })
}

/**
 * 根据id获取面试题详情
 * @param {*} interviewId 
 */
function getInterviewById(interviewId) {
  return request(`/api/interview/${interviewId}`, {
    method: 'GET'
  })
}

/**
 * 编辑面试题
 */
function editInterview(interviewId, data) {
  return request(`/api/interview/${interviewId}`, {
    method: 'PATCH',
    data: {
      ...data
    }
  })
}


export default {
  addInterview,
  getInterviewByPage,
  deleteInterview,
  getInterviewById,
  editInterview
}