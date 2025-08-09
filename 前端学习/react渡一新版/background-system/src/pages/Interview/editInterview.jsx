import React, { useState, useEffect } from 'react';
import InterviewForm from './components/interviewForm';
import { useParams, useNavigate } from 'react-router-dom';
import InterviewController from '@/services/interview';
import { message } from 'antd';

// 编辑面试题
function EditInterview(props) {
  const { id } = useParams();
  const [interviewInfo, setInterviewInfo] = useState(null);
  const navigate = useNavigate();

  // 根据传过来的id查询内容
  useEffect(() => {
    async function fetchData() {
      const { data } = await InterviewController.getInterviewById(id);
      console.log('data是', data)
      setInterviewInfo(data);
    }
    fetchData();
  }, [])

  // 修改面试题
  function submitHandle(interviewContent) {
    InterviewController.editInterview(id, {
      interviewTitle: interviewInfo.interviewTitle,
      interviewContent,
      typeId: interviewInfo.typeId
    })

    navigate('/interview/interviewList')
    message.success('修改题目成功')
  }

  return (
    <div className='container' style={{ width: 1000 }}>
      <InterviewForm
        type='edit'
        submitHandle={submitHandle}
        interviewInfo={interviewInfo}
        setInterviewInfo={setInterviewInfo}
      />
    </div>
  );
}

export default EditInterview;