import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getIssueById } from '../api/issue';
import { getUserById } from '../api/user';
import PageHeader from '../components/PageHeader';
import Recommend from '../components/Recommand';
import ScoreRank from '../components/ScoreRank';
import styles from '../css/IssueDetail.module.css';
import { formatDate } from '../utils/tools';
import { Avatar } from 'antd';
import Discuss from '../components/Discuss';

/**
 * 问答详情
 * @param {*} props 
 * @returns 
 */
function IssueDetail(props) {
  const { id } = useParams();
  const [issueInfo, setIssueInfo] = useState(null);
  const [issueUser, setIssueUser] = useState(null);

  useEffect(() => {
    async function fetchData() {
      const { data } = await getIssueById(id);
      setIssueInfo(data);
      const result = await getUserById(data.userId);
      setIssueUser(result.data);
    }
    fetchData();
  }, []);


  return (
    <div className={styles.container}>
      <PageHeader title="问题详情" />
      <div className={styles.detailContainer}>
        {/* 左侧 */}
        <div className={styles.leftSide}>
          {/* 上方显示问答详情 */}
          <div className={styles.question}>
            <h1>{issueInfo?.issueTitle}</h1>
            {/* 提问人信息 */}
            <div className={styles.questioner}>
              <Avatar src={issueUser?.avatar} size="small"></Avatar>
              <span className={styles.user}>{issueUser?.nickname}</span>
              <span>发布于：{formatDate(issueInfo?.issueDate)}</span>
            </div>
            {/* 问题详情 */}
            <div className={styles.content}>
              <div dangerouslySetInnerHTML={{ __html: issueInfo?.issueContent }}></div>
            </div>
          </div>
          {/* 评论 */}
          {issueInfo && (
            <Discuss
              commentType={1}
              targetId={issueInfo._id}
            />
          )}
        </div>
        {/* 右侧 */}
        <div className={styles.rightSide}>
          <div style={{ marginBottom: 20 }}>
            <Recommend />
          </div>

          <div style={{ marginBottom: 20 }}>
            <ScoreRank />
          </div>
        </div>
      </div>
    </div>
  );
}

export default IssueDetail;