import { useRef, useState, useEffect } from 'react';
import { Form, Input, Select, Button, message } from 'antd';
import styles from '../css/AddIssue.module.css';
import { useSelector, useDispatch } from 'react-redux';
import '@toast-ui/editor/dist/toastui-editor.css';
import { Editor } from '@toast-ui/react-editor';
import { typeOptionCreator } from '../utils/tools';
import { getTypeList } from '../redux/typeSlice';
import { addIssue } from '../api/issue';
import { useNavigate } from 'react-router-dom';

function AddIssue(props) {

  const formRef = useRef();
  const editorRef = useRef();
  const navigate = useNavigate();
  const [issueInfo, setIssueInfo] = useState({
    issueTitle: "",
    issueContent: "",
    typeId: "",
    userId: ''
  })


  const dispatch = useDispatch();
  const { typeList } = useSelector(state => state.type);
  const { userInfo } = useSelector(state => state.user);
  useEffect(() => {
    if (!typeList.length) {
      dispatch(getTypeList());
    }
  })

  /**
   * 提交问答的函数
   */
  function addHandle() {
    const content = editorRef.current.getInstance().getHTML();

    addIssue({
      issueTitle: issueInfo.issueTitle,
      issueContent: content,
      userId: userInfo._id,
      typeId: issueInfo.typeId
    }).then(() => {
      // 消息展示
      message.success('文章已提交，审核之后将会展示给其他用户');
      navigate("/");
    })
  }

  function updateInfo(newContent, key) {
    const newIssueInfo = { ...issueInfo };
    newIssueInfo[key] = newContent;
    setIssueInfo(newIssueInfo);
  }

  /**
   * 下拉列表选项改变出发回调
   */
  function handleChange(value) {
    updateInfo(value, "typeId");
  }
  return (
    <div className={styles.container}>
      {contextHolder}
      <Form
        name="basic"
        initialValues={issueInfo}
        autoComplete="off"
        ref={formRef}
        onFinish={addHandle}
      >
        {/* 问答标题 */}
        <Form.Item
          label="标题"
          name="issueTitle"
          rules={[{ required: true, message: '请输入标题' }]}
        >
          <Input
            placeholder="请输入标题"
            size="large"
            value={issueInfo.issueTitle}
            onChange={(e) => updateInfo(e.target.value, 'issueTitle')}
          />
        </Form.Item>

        {/* 问题类型 */}
        <Form.Item
          label="问题分类"
          name="typeId"
          rules={[{ required: true, message: '请选择问题所属分类' }]}
        >
          <Select
            style={{ width: 200 }}
            onChange={handleChange}>
            {typeOptionCreator(Select, typeList)}
          </Select>
        </Form.Item>


        {/* 问答内容 */}
        <Form.Item
          label="问题描述"
          name="issueContent"
          rules={[{ required: true, message: '请输入问题描述' }]}
        >
          <Editor
            initialValue=""
            previewStyle="vertical"
            height="600px"
            initialEditType="wysiwyg"
            useCommandShortcut={true}
            language='zh-CN'
            ref={editorRef}
          />
        </Form.Item>


        {/* 确认按钮 */}
        <Form.Item wrapperCol={{ offset: 3, span: 16 }}>
          <Button type="primary" htmlType="submit">
            确认新增
          </Button>

          <Button type="link" htmlType="submit" className="resetBtn">
            重置
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}

export default AddIssue;