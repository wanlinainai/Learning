import { useState, useEffect } from 'react';
import { getUserByPointsRank } from '../api/user';
import ScoreItem from './ScoreItem';
import { Card } from 'antd';

/**
 * 积分排名
 * @param {*} props 
 * @returns 
 */
function ScoreRank(props) {

  const [userRankInfo, setUserRankInfo] = useState([]);// 存储用户排名信息

  useEffect(() => {
    async function fetchUser() {
      const { data } = await getUserByPointsRank();
      setUserRankInfo(data)
    }
    fetchUser();
  }, []);

  const userPointerRankArr = []

  if (userRankInfo.length) {
    for (let i = 0; i < userRankInfo.length; i++) {
      userPointerRankArr.push(
        <ScoreItem
          rankInfo={userRankInfo[i]}
          rank={i + 1}
          key={userRankInfo[i]._id}
        />
      )
    }
  }

  return (
    <div>
      <Card title="积分排行榜">
        {userPointerRankArr}
      </Card>
    </div>
  );
}

export default ScoreRank;