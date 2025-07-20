import request from './request';


/**
 * 分页获取问答
 */
export function getIssueByPage(params) {
  return request({
    url: '/api/issue',
    method: 'GET',
    params: {
      ...params // 展开参数params
    }
  })
}

/**
 * 新增问答
 */
export function addIssue(newIssue) {
  return request({
    url: '/api/issue/',
    method: 'post',
    data: newIssue
  })
}