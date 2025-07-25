import React from 'react';
import styles from '../css/PageHeader.module.css';

/**
 * 每一页的页头
 * @param  props 
 * @returns 
 */
function PageHeader(props) {
  return (
    <div className={styles.row}>
      {/* 文字展示 */}
      <div className={styles.pageHeader}>
        {props.title}
      </div>

      {/* 分类选择 */}
      {props.children}
    </div>
  );
}

export default PageHeader;