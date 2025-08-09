import React, { useState } from 'react';
import InterviewForm from './components/interviewForm';
import InterviewController from '@/services/interview';
import { useNavigate } from '@umijs/max';
import { message } from 'antd';

/**
 * 添加面试题
 * @returns 
 */
function AddInterview() {

  const navigate = useNavigate();

  const [newInterviewInfo, setInterviewInfo] = useState({
    interviewTitle: '',
    interviewContent: '',
    typeId: ''
  });

  /**
   * 新增面试题
   */
  function submitHandle(interviewContent) {
    InterviewController.addInterview({
      interviewTitle: newInterviewInfo.interviewTitle,
      interviewContent,
      typeId: newInterviewInfo.typeId
    })

    // 跳转首页
    navigate('/interview/interviewList')
    message.success('新增题目成功')
  }

  return (
    <div className='container' style={{ width: 1000 }}>
      <InterviewForm
        type="add"
        submitHandle={submitHandle}
        interviewInfo={newInterviewInfo}
        setInterviewInfo={setInterviewInfo}
      />
    </div>
  );
}

export default AddInterview;