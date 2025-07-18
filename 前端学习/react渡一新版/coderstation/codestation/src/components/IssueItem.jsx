import {useEffect, useState} from 'react';
import styles from '../css/IssueItem.module.css'
import { formatDate } from '../utils/tools';
import { useDispatch, useSelector } from 'react-redux';
import { getTypeList } from '../redux/typeSlice';
import { Tag } from 'antd';
import {getUserById} from '../api/user';

/**
 * 每一条问答的项目
 * @param {*} props 
 * @returns 
 */
function IssueItem(props) {
  // 存储用户信息
  const [userInfo, setUserInfo] = useState([]);

  const dispatch = useDispatch();
  const {typeList} = useSelector(state => state.type)

  const colorArr = ['#108ee9', '#2db7f5', '#f50', 'green', '#87d068', 'blue', 'red', 'purple'];

  useEffect(()=> {
    if(!typeList.length) {
      // 派发 Action 来发送请求，获取到数据填充到状态仓库
      dispatch(getTypeList())
    }

    // 发送请求获取用户信息
    async function fetchUserData() {
      const {data} = await getUserById(props.issueInfo.userId);
      setUserInfo(data)
    }
    fetchUserData();
  }, [])

  const type = typeList.find(item => item._id === props.issueInfo.typeId)

  return (
    <div className={styles.container}>
      {/* 回答数 */}
      <div className={styles.issueNum}>
        <div>{props.issueInfo.commentNumber}</div>
        <div>回答</div>
      </div>
      {/* 浏览数 */}
      <div className={styles.issueNum}>
        <div>{props.issueInfo.scanNumber}</div>
        <div>浏览</div>
      </div>
      {/* 问题内容 */}
      <div className={styles.issueContainer}>
        <div className={styles.top}>{props.issueInfo.issueTitle}</div>
        <div className={styles.bottom}>
          {/* 标签类型 */}
          <div className={styles.left}>
            <Tag color={colorArr[typeList.indexOf(type) % colorArr.length]}>{type?.typeName}</Tag>
          </div>
          {/* 名称、时间 */}
          <div className={styles.right}>
            <Tag color='volcano'>{userInfo.nickname}</Tag>
            <span>{formatDate(props.issueInfo.issueDate, "year")}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default IssueItem;