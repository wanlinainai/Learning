import { request } from 'umi';

/**
 * 新增书籍
 */
function addBook(newBookInfo) {
  return request('/api/book', {
    method: 'post',
    data: newBookInfo
  })
}

export default {
  addBook
}