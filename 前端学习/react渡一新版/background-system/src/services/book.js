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


/**
 * 获取书籍列表
 * @param {*} param 
 */
function getBookByPage(param) {
  return request('/api/book', {
    method: 'GET',
    params: {
      ...param
    }
  })
}

/**
 * 删除书籍
 * @param {} bookId 
 * @returns 
 */
function deleteBook(bookId) {
  return request(`/api/book/${bookId}`, {
    method: 'delete'
  })
}

/**
 * 通过Id获取书籍信息
 * @param {*} bookId 
 * @returns 
 */
function getBookById(bookId) {
  return request(`/api/book/${bookId}`, {
    method: 'GET'
  })
}

/**
 * 编辑书籍
 * @param {*} bookId 
 * @param {*} bookInfo 
 */
function editBook(bookId, bookInfo) {
  return request(`/api/book/${bookId}`, {
    method: 'PATCH',
    data: bookInfo
  })
}
export default {
  addBook,
  getBookByPage,
  deleteBook,
  getBookById,
  editBook
}