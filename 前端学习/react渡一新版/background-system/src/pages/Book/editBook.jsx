import { useEffect, useState } from 'react';
import {useNavigate, useParams} from 'react-router-dom';
import BookController from '@/services/book';
import { message } from 'antd';
import BookForm from './components/bookForm';

/**
 * 编辑图书组件
 * @param {*} props 
 * @returns 
 */
function EditBook(props) {
  const {id} = useParams();
  const [bookInfo, setBookInfo] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchData() {
      // 根据问答ID获取该问答具体的信息
      const {data} = await BookController.getBookById(id);
      setBookInfo(data);
    }
    fetchData();
  }, []);

  /**
   * 提交处理函数
   */
  function submitHandle(bookIntro) {
    BookController.editBook(id, {
      bookTitle: bookInfo.bookTitle,
      bookIntro,
      downloadLink: bookInfo.downloadLink,
      requirePoints:bookInfo.requirePoints,
      bookPic: bookInfo.bookPic,
      typeId: bookInfo.typeId,
    });

    navigate('/book/bookList');
    message.success('书籍信息修改成功');
  }

  return (
    <>
      <div className='container'style={{width: 800}}>
        <BookForm 
          type="edit"
          bookInfo={bookInfo}
          setBookInfo = {setBookInfo}
          submitHandle={submitHandle}
        />
    </div>
    </>
  );
}

export default EditBook;