import { typeOptionCreator } from '@/utils/tools';
import { Editor } from '@toast-ui/react-editor';
import { useDispatch, useSelector } from '@umijs/max';
import { Button, Form, Input, Select } from 'antd';
import { useRef, useState } from 'react';

/**
 * 面试题表单组件
 * @param {*} props 
 * @returns 
 */
function InterviewForm(props) {
  const { type, submitHandle, interviewInfo, setInterviewInfo } = props;
  const dispatch = useDispatch();
  const formRef = useRef();
  const editorRef = useRef();

  const { typeList } = useSelector((state) => state.type || []);

  const [firstIn, setFirstIn] = useState(true);

  // 如果typeList为空，初始化
  if (!typeList.length) {
    dispatch({
      type: 'type/_initTypeList'
    })
  }

  // 如果是编辑的话需要扎实内容
  if (type === 'edit') {
    if (formRef.current && firstIn) {
      setFirstIn(false);
      editorRef.current.getInstance().setHTML(interviewInfo?.interviewContent);
    }
    if (formRef.current) {
      formRef.current.setFieldsValue(interviewInfo);
    }
  }

  function addHandle() {
    const content = editorRef.current.getInstance().getHTML();
    submitHandle(content);
  }

  const handleChange = (value) => {
    updateInfo(value, 'typeId')
  }

  // 更新信息
  function updateInfo(newInfo, key) {
    const newInterviewInfo = { ...interviewInfo };
    if (typeof newInfo === 'string') {
      newInterviewInfo[key] = newInfo.trim();
    } else {
      newInterviewInfo[key] = newInfo;
    }
    setInterviewInfo(newInterviewInfo);
  }

  return (
    <Form
      name='basic'
      initialValues={interviewInfo}
      autoComplete='off'
      ref={formRef}
      onFinish={addHandle}
    >

      <Form.Item
        label='题目标题'
        name="interviewTitle"
        rules={[
          { required: true, message: '请输入题目标题' }
        ]}
      >
        <Input
          placeholder='请填写题目标题'
          value={interviewInfo?.interviewTitle}
          onChange={(e) => updateInfo(e.target.value, 'interviewTitle')}
        />
      </Form.Item>

      <Form.Item
        label="题目分类"
        name='typeId'
        rules={[{ required: true, message: '请选择题目所属分类' }]}
      >
        <Select style={{ width: 200 }} onChange={handleChange}>
          {typeOptionCreator(Select, typeList)}
        </Select>
      </Form.Item>

      <Form.Item
        label='题目内容'
        name="interviewContent"
        rules={[{ required: true, message: '请输入题目解答' }]}
      >
        <Editor
          initialValue=''
          previewStyle='vertical'
          height='600px'
          initialEditType='markdown'
          useCommandShortcut={true}
          language='zh-CN'
          ref={editorRef}
        />
      </Form.Item>

      <Form.Item>
        <Button
          type='primary'
          htmlType='submit'
        >{type === 'add' ? '新增' : '修改'}</Button>

        <Button type='link' htmlType='submit' className='resetBtn'>重置</Button>
      </Form.Item>

    </Form>
  );
}

export default InterviewForm;