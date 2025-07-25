import React from 'react';
import styles from '../css/PersonalInfoItem.module.css';

/**
 * 个人信息的简介组件
 * @param {*} props 
 * @returns 
 */
function PersonalInfoItem(props) {
  return (
    <div className={styles.infoContainer}>
      <div className={styles.left}>
        <div>{props.info.itemName}：</div>
        <div>{props.info.itemValue}</div>
      </div>
    </div>
  );
}

export default PersonalInfoItem;