import { useState } from "react";

// 自定义Hook --> 使用了原有的useState这个Hook，这个也是一个Hook
function useMyBook() {
  const [bookName, setBookName] = useState("React learning...")
  return {
    bookName, setBookName
  }
}

export default useMyBook;