import {useState, useEffect} from 'react';
import PageHeader from '../components/PageHeader';
import styles from '../css/Issue.module.css';
import { getIssueByPage } from '../api/issue';
import IssueItem from '../components/IssueItem';

function Issues(props) {

  const [pageInfo, setPageInfo] = useState({
    current: 1, // 当前页
    pageSize: 15, // 一页显示15条
    total: 0
  })

  // 存储获取到的状态资源列表
  const [issueInfo, setIssueInfo] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const {data} = await getIssueByPage({
        current: pageInfo.current,
        pageSize: pageInfo.pageSize,
        issueStatus: true
      });
      
      setIssueInfo(data.data);
      setPageInfo({
        current: data.currentPage,
        pageSize: data.eachPage,
        total: data.count
      })
    }
    fetchData();
  }, [pageInfo.current, pageInfo.pageSize]);

  let issueList = [];
  for(let i = 0; i < issueInfo.length; i++) {
    issueList.push(<IssueItem key={i} issueInfo={issueInfo[i]}/>)
  }



  return (
    <div className={styles.container}>
      {/* 上面的头部 */}
      <PageHeader title="问答列表"/>
      {/* 下面的列表内容区域 */}
      <div className={styles.issueContainer}>
        {/* 左边区域 */}
        <div className={styles.leftSide}>
          {issueList}
        </div>
        {/* 右边区域 */}
        <div className={styles.rightSide}></div>
      </div>
    </div>
  );
}

export default Issues;