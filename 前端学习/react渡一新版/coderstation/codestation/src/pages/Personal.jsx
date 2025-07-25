import React, { useState } from 'react';
import PageHeader from '../components/PageHeader';
import styles from '../css/Personal.module.css';
import { useSelector } from 'react-redux';
import { Card, Image, Upload,Modal } from 'antd';
import PersonalInfoItem from '../components/PersonalInfoItem';
import { formatDate } from '../utils/tools';
import {PlusOutlined} from '@ant-design/icons';
import { updateUserInfoAsync } from '../redux/userSlice';
import { useDispatch } from 'react-redux';

/**
 * 个人中心
 * @param {*} props 
 * @returns 
 */
function Personal(props) {

  const {userInfo} = useSelector(state => state.user);
  const dispatch = useDispatch();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [panelName, setPanelName] = useState("");


  const showModal = (name) => {
    setPanelName(name)
    setIsModalOpen(true);
  };

  const handleOk = () => {
    setIsModalOpen(false);
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  function handleAvatar(newURL, key) {
    // 将仓库和服务器端的数据一并更新
    dispatch(updateUserInfoAsync({
      userId: userInfo._id,
      newInfo: {
        [key]: newURL
      }
    }))
  }


  return (
    <div>
      <PageHeader title="个人中心"/>
      {/* 信息展示 */}
      <div className={styles.container}>
        {/* 基本信息 */}
        <div className={styles.row}>
          <Card title="基本信息" extra={(<div className={styles.edit} onClick={() => showModal("基本信息")}>编辑</div>)}>
            <PersonalInfoItem info={{itemName : "登录账号", itemValue: userInfo.loginId}}/>
            <PersonalInfoItem info={{itemName : "账号密码", itemValue: '**** **** ***'}}/>
            <PersonalInfoItem info={{itemName: "用户昵称", itemValue: userInfo.nickname}}/>
            <PersonalInfoItem info={{itemName: "用户积分", itemValue: userInfo.points}}/>
            <PersonalInfoItem info={{itemName: "注册时间", itemValue: formatDate(userInfo.registerDate)}} />
            <PersonalInfoItem info={{itemName: "上次登录时间", itemValue: formatDate(userInfo.lastLoginDate)}} />
            <div style={{fontWeight: '100', height: "50px"}}>当前头像</div>
            <Image src={userInfo.avatar} width={100}/>
            <div style={{fontWeight: '100', height: "50px"}}>上传新头像</div>
            <Upload
              action='/api/upload'
              maxCount={1}
              listType='picture-card'
              onChange={(e) => {
                if(e.file.status === 'done') {
                  // 上传完成
                  const url = e.file.response.data;
                  // 处理用户头像更新
                  handleAvatar(url, 'avatar');
                }
              }}
            >
              <PlusOutlined/>
            </Upload>
          </Card>
        </div>
        {/* 社交账号 */}
        <div className={styles.row}>
          <Card title="社交账号" extra={(<div className={styles.edit} onClick={() => showModal("社交账号")}>编辑</div>)}></Card>
        </div>
        {/* 个人简介 */}
        <div className={styles.row}>
          <Card title="个人简介" extra={(<div className={styles.edit} onClick={() => showModal("个人简介")}>编辑</div>)}></Card>
        </div>
      </div>

      {/* 修改信息的对话框 */}
      <Modal title={panelName} open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
        <p>Some contents...</p>
        <p>Some contents...</p>
        <p>Some contents...</p>
      </Modal>
    </div>
  );
}

export default Personal;