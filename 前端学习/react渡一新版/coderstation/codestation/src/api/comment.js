import request from './request';

/**
 * 根据问答的id获取对应的评论
 * @param {*} id 
 * @param {*} params 
 * @returns 
 */
export function getIssueCommentById(id, params) {
  return request({
    url: `/api/comment/issuecomment/${id}`,
    method: 'GET',
    params: {
      ...params
    }
  })
}

/**
 * 添加新评论
 * @param {*} newComment 
 * @returns 
 */
export function addComment(newComment) {
  return request({
    url: '/api/comment',
    method: 'post',
    data: newComment
  })
}