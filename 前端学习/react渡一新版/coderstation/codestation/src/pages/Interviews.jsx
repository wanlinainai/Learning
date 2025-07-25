import React, { useEffect } from 'react';
import { getInterviewTitleAsync } from '../redux/interviewSlice';
import { useSelector, useDispatch } from 'react-redux';
import {getTypeList} from '../redux/typeSlice';

function Interviews(props) {
  const dispatch = useDispatch();
  const {interviewTitleList} = useSelector(state => state.interview);
  const {typeList} = useSelector(state => state.type);

  useEffect(() => {
    if(interviewTitleList.length) {
      // 初始化仓库中的面试题标题
      dispatch(getInterviewTitleAsync())
    }
    // 分类名
    if(!typeList.length) {
      dispatch(getTypeList())
    }

    
    
  }, [])

  return (
    <div>
      面试题
    </div>
  );
}

export default Interviews;