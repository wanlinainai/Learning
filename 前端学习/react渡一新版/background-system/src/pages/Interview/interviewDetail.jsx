import { useDispatch, useParams, useSelector } from '@umijs/max';
import { Card, Tag } from 'antd';
import React, { useEffect, useState } from 'react';
import InterviewController from '@/services/interview';

function InterviewDetail(props) {
  const { id } = useParams();
  const [interviewInfo, setInterviewInfo] = useState({});
  const [typeName, setTypeName] = useState(null);
  const dispatch = useDispatch();

  const { typeList } = useSelector((state) => state.type);
  if (!typeList.length) {
    dispatch({
      type: 'type/_initTypeList'
    })
  }

  useEffect(() => {
    async function fetchData() {
      const { data } = await InterviewController.getInterviewById(id);
      setInterviewInfo(data);
      // 获取typeId对应的 typeName
      const type = typeList.find((item) => item._id === data.typeId);
      setTypeName(type?.typeName)
    }
    fetchData()
  }, []);

  return (
    <div>
      <Card
        title={interviewInfo?.interviewTitle}
        style={{
          marginBottom: 10
        }}
        extra={
          <Tag color='purple' key={interviewInfo?.typeId}>
            {typeName}
          </Tag>
        }
      >
        <div
          dangerouslySetInnerHTML={{ __html: interviewInfo?.interviewContent }}
        ></div>
      </Card>
    </div>
  );
}

export default InterviewDetail;