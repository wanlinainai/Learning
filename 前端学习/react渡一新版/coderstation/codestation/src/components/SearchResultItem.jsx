import React from 'react';
import IssueItem from './IssueItem';

/**
 * 存储搜索结果的组件(根据搜索的类型返回不同类型的搜索项目组件 IssueItem / BookItem).
 * 通常没有自己的JSX文件，一般是用于容器组件
 * @param {*} props 
 * @returns 
 */
function SearchResultItem(props) {
  return (
    <div>
      {
        props.info.issueTitle ? <IssueItem issueInfo={props.info}/>
        : null
      }
    </div>
  );
}

export default SearchResultItem;