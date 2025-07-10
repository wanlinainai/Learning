import { useState, useEffect } from 'react';
import { getStuListApi } from '../api/stuApi';
import Alert from './Alert';
import { useLocation } from 'react-router-dom';
import { NavLink } from 'react-router-dom';

function Home(props) {

  const [stuList, setStuList] = useState([]) // 存储所有的数据
  const [searchItem, setSearchItem] = useState("")
  const [alert, setAlert] = useState(null)
  const [searchList, setSearchList] = useState([]) // 存储搜索之后的数据

  const location = useLocation();

  // 需要添加上依赖项为空数组，代表只执行一次
  useEffect(() => {
    getStuListApi().then(({ data }) => {
      setStuList(data)
    })
  }, [])

  // 加一个副作用effect，用于接收传递过来的参数state
  useEffect(() => {
    if(location.state) {
      setAlert(location.state)
    }
  }, [location])

  function changeHandle() {

  }

  const showAlert = alert ? <Alert {...alert}/> : null;


  function changeHandle(name) {
    // 用户要搜索的内容，存储到了searchItem里面
      setSearchItem(name)
    // 接下来进行简单的过滤
    const arr = stuList.filter((item) => {
      return item.name.match(name);
    });
    setSearchList(arr)
  }

  // list就是最终要显示的列表
  const list=  searchItem ? searchList : stuList;

    const trs = list.map((item, index) => {
    return (
      <tr key={index}>
        <td>{item.name}</td>
        <td>{item.age}</td>
        <td>{item.phone}</td>
        <td>
          <NavLink to={`/detail/${item.id}`}>详情</NavLink>
        </td>
      </tr>
    )
  })

  return (
    <div>
      {showAlert}
      <h1>学生列表</h1>
      <input
        type="text"
        placeholder='搜索看看'
        value={searchItem}
        onChange={(e) => {changeHandle(e.target.value)}}
        className='form-control'
      />
      {/* 表格 */}
      <table className='table table-striped'>
        <thead>
          <tr>
            <th>姓名</th>
            <th>年龄</th>
            <th>联系方式</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          {trs}
        </tbody>
      </table>
    </div>
  );
}

export default Home;