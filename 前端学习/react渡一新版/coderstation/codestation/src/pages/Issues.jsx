import { useState, useEffect } from 'react';
import PageHeader from '../components/PageHeader';
import styles from '../css/Issue.module.css';
import { getIssueByPage } from '../api/issue';
import IssueItem from '../components/IssueItem';
import { Pagination } from 'antd';
import AddIssueBtn from '../components/AddIssueBtn';
import Recommand from '../components/Recommand';
import ScoreRank from '../components/ScoreRank';
import TypeSelect from '../components/TypeSelect';
import { useSelector } from 'react-redux';


function Issues(props) {

  const [pageInfo, setPageInfo] = useState({
    current: 1, // 当前页
    pageSize: 15, // 一页显示15条
    total: 0
  })

  // 从状态仓库获取当前是否有typeId的值
  const {issueTypeId} = useSelector(state => state.type);

  // 存储获取到的状态资源列表
  const [issueInfo, setIssueInfo] = useState([]);

  useEffect(() => {
    async function fetchData() {
      let searchParams = {
        current: pageInfo.current,
        pageSize: pageInfo.pageSize,
        issueStatus: true
      } 

      if(issueTypeId !== 'all') {
        // 存在分类
        searchParams.typeId = issueTypeId
        // 如果按照分类进行查询，需要重新将当前页设置成第一页
        searchParams.current = 1
      }

      const { data } = await getIssueByPage(searchParams);

      setIssueInfo(data.data);
      setPageInfo({
        current: data.currentPage,
        pageSize: data.eachPage,
        total: data.count
      })
    }
    fetchData();
  }, [pageInfo.current, pageInfo.pageSize, issueTypeId]);

  let issueList = [];
  for (let i = 0; i < issueInfo.length; i++) {
    issueList.push(<IssueItem key={i} issueInfo={issueInfo[i]} />)
  }

  function handleChangePage(current, pageSize) {
    setPageInfo({
      current,
      pageSize
    })
  }


  return (
    <div className={styles.container}>
      {/* 上面的头部 */}
      <PageHeader title="问答列表">
        <TypeSelect/>
      </PageHeader>
      {/* 下面的列表内容区域 */}
      <div className={styles.issueContainer}>
        {/* 左边区域 */}
        <div className={styles.leftSide}>
          {issueList}
          {issueInfo.length > 0 ? (
            <div className='paginationContainer'>
            <Pagination
              showQuickJumper
              defaultCurrent={1}
              {...pageInfo}
              onChange={handleChangePage}
              pageSizeOptions={[10, 20, 30]}
              showSizeChanger
            />
          </div>
          ) : (
            <div className={styles.noIssue}>有问题，就来Code Station</div>
          )}
          
        </div>
        {/* 右边区域 */}
        <div className={styles.rightSide}>
          <AddIssueBtn />
          <div>
            <Recommand/>
          </div>
          <ScoreRank/>
        </div>
      </div>
    </div>
  );
}

export default Issues;