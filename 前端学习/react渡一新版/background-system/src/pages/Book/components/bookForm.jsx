import { PlusOutlined } from '@ant-design/icons';
import { Editor } from '@toast-ui/react-editor';
import { Button, Form, Image, Input, Select, Upload } from 'antd';
import { useRef } from 'react';
import {useDispatch, useSelector} from '@umijs/max';

/**
 * 新增书籍组件
 * @param {*} props 
 * @returns 
 */
function BookForm(props) {

  const {bookInfo, setBookInfo, type, submitHandle} = props;
  const formRef = useRef();
  const editorRef = useRef();

  const [firstIn, setFirstIn] = useState(true);

  const dispatch = useDispatch();

  // 书籍封面
  let bookPicPreview = null;
  if(type === 'edit') {
    bookPicPreview = (
      <Form.Item label="当前封面" name="bookPicPreView">
        <Image src={bookInfo?.bookPic} width={100}/>
      </Form.Item>
    )
  }

  const {typeList} = useSelector(state => state.type);
  // 如果类型列表为空，初始化一次
  if(!typeList.length) {
    dispatch({
      type: 'type/_initTypeList'
    })
  }

  /**
   * 更新操作
   */
  function updateInfo(newInfo, key) {
    const newBookInfo = { ...bookInfo };
    if(typeof newInfo === 'string') {
      newBookInfo[key] = newInfo.trim();
    } else {
      newBookInfo[key] = newInfo;
    }
    setBookInfo(newBookInfo);
  }

  const handleTypeChange = (value) => {
    updateInfo(value, "typeId");
  }

  const handlePointChange = (value) => {
    updateInfo(value, "requirePoints");
  }

  function addHandle() {
    const content = editorRef.current.getInstance().getHTML();
    submitHandle(content);
  }

  return (
    <div>
      <Form 
        name='basic'
        initialValues={bookInfo}
        autoComplete='off'
        ref={formRef}
        onFinish={addHandle}
      >
        <Form.Item
          label="书籍标题"
          name="bookTitle"
          rules={[{required: true, message: '请输入书名'}]}
        >
          <Input value={bookInfo?.bookTitle} onChange={(e) => updateInfo(e.target.value, "bookTitle")}/>
        </Form.Item>

        <Form.Item
          label="书籍介绍"
          name="bookIntro"
          rules={[{required: true, message:"请输入书籍相关的介绍"}]}
        >
          <Editor 
            initialValues=""
            previewStyle="vertical"
            height="600px"
            initialEditType="markdown"
            useCommandShortcut={true}
            language="zh-CN"
            placeholder="请输入书籍相关的介绍"
            ref={editorRef}
          />
        </Form.Item>

        <Form.Item
          label="下载链接"
          name="downloadLink"
          rules={[
            {required: true, message: '请输入书籍链接'}
          ]}
        >
          <Input 
            value={bookInfo?.downloadLink}
            onChange={(e) => updateInfo(e.target.value, 'downloadLink')}
          />
        </Form.Item>

        <Form.Item
          label="所需积分"
          name="requirePoints"
          rules={[
            {require: true, message: '请选择下载需要的积分'}
          ]}
        >
          <Select style={{width: 200}} onChange={handlePointChange}>
            <Select.Option value={20} key={20}>20</Select.Option>
            <Select.Option value={30} key={30}>30</Select.Option>
            <Select.Option value={40} key={40}>40</Select.Option>
          </Select>
        </Form.Item>

        <Form.Item
          label="书籍分类"
          name="typeId"
          rules={[
            {required: true, message: '请选择书籍分类'}
          ]}
        >
          <Select style={{width: 200}} onChange={handleTypeChange}>
            {typeOptionCreator(Select, typeList)}
          </Select>
        </Form.Item>

        {bookPicPreview}

        <Form.Item
          label="书籍封面"
          valuePropName='fileList'
        >
          <Upload
            action="/api/uplaod"
            listType='picture-card'
            maxCount={1}
            onChange={(e) => {
              if(e.file.status === 'done') {
                // 上传完成
                const url = e.file.response.data;
                updateInfo(url, "bookPic");
              }
            }}
          >
            <PlusOutlined/>
          </Upload>
        </Form.Item>

        <Form.Item wrapperCol={{offset: 3, span: 16}}>
          <Button type='primary' htmlType='submit'>
            {type === 'add' ? '确认新增': '修改'}
          </Button>

          <Button type='link' htmlType='submit' className='resetBtn'>重置</Button>
        </Form.Item>
      </Form>
    </div>
  );
}

export default BookForm;