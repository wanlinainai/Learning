import request from './request.js';

/**
 * 获取所有分类对应的面试题标题
 */
export function getInterviewTitle() {
  return request({
    url: '/api/interview/interviewTitle',
    method: 'GET'
  })
}


/**
 * 根据面试题id获取面试题
 */
export function getInterviewById(interviewId) {
  return request({
    url: `/api/interview/${interviewId}`,
    method: 'GET'
  })
}