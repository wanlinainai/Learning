import { useState } from 'react';
import BookForm from './components/bookForm';

import BookController from '../../services/book';
import { useNavigate } from '@umijs/max';
import { message } from 'antd';

function AddBook(props) {

  const [newBookInfo, setNewBookInfo] = useState({
    bookTitle: '',
    bookIntro: '',
    downloadLink: '',
    requirePoints:'',
    bookPic: '',
    typeId: '',
  })

  const navigate = useNavigate();

  /**
   * 用户点击新增书籍
   */
  function submitHandle(bookIntro) {
    BookController.addBook({
      bookTitle: newBookInfo.bookTitle,
      bookIntro,
      downloadLink: newBookInfo.downloadLink,
      requirePoints:newBookInfo.requirePoints,
      bookPic: newBookInfo.bookPic,
      typeId: newBookInfo.typeId,
    })

    // 跳转回首页
    navigate('/book/bookList');
    message.success('新增书籍成功');
  }

  return (
    <div className='container'style={{width: 1000}}>
      <BookForm 
        type="add"
        bookInfo={newBookInfo}
        setBookInfo = {setNewBookInfo}
        submitHandle={submitHandle}
      />
    </div>
  );
}

export default AddBook;