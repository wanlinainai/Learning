import { useEffect, useRef, useState } from 'react';
import { Avatar, Form, Button, List, Comment, Tooltip, message } from 'antd';
import { useSelector } from 'react-redux';
import { UserOutlined } from '@ant-design/icons';
import { Editor } from '@toast-ui/react-editor';
import '@toast-ui/editor/dist/toastui-editor.css';
import { getIssueCommentById } from '../api/comment';
import { getUserById } from '../api/user';
import { formatDate } from '../utils/tools';

/**
 * 评论组件
 * @param {*} props 
 * @returns 
 */
function Discuss(props) {
  const { userInfo, isLogin } = useSelector(state => state.user);
  const [commentList, setCommentList] = useState([]);
  const [pageInfo, setPageInfo] = useState({
    current: 1,
    pageSize: 10,
    total: 0
  })
  const editorRef = useRef();


  useEffect(() => {
    async function fetchCommentList() {
      // 添加安全检查
      if (!props.targetId) return;

      let data = null;
      if (props.commentType === 1) {
        // 获取问答的Id
        const result = await getIssueCommentById(props.targetId, {
          current: pageInfo.current,
          pageSize: pageInfo.pageSize
        });
        data = result.data;
      } else if (props.commentType === 2) {
        // 书籍的评论
      }

      // 添加数据存在性检查
      if (data && data.data && data.data.length > 0) {
        for (let i = 0; i < data.data.length; i++) {
          const result = await getUserById(data.data[i].userId);
          data.data[i].userInfo = result.data;
        }
        // 更新评论数据
        setCommentList(data.data);
        // 更新分页数据
        setPageInfo({
          current: data.currentPage,
          eachPage: data.eachPage,
          count: data.count,
          total: data.totalPage
        });
      }
    }
    fetchCommentList();
  }, [props.targetId])

  // 头像处理
  let avatar = null;
  if (isLogin) {
    avatar = (
      <Avatar src={userInfo?.avatar} />
    )
  } else {
    avatar = (
      <Avatar icon={<UserOutlined />} />
    )
  }

  /**
   * 添加评论
   */
  function onSubmit() {
    let newComment = null;
    if (props.commentType === 1) {
      newComment = editorRef.current?.getInstance().getHTML();
      console.log('编辑器内容:', newComment); // 调试日志
      if (newComment === '<p><br></p>' || newComment === '<p></p>') {
        newComment = ''
      }
    } else if (props.commentType === 2) {

    }

    if (!newComment) {
      console.log('显示警告消息'); // 调试日志
      message.warning('请输入评论内容');
      return;
    }
  }

  return (
    <div>
      {/* 评论框 */}
      <Comment
        avatar={avatar}
        content={
          <>
            <Form.Item>
              <Editor
                initialValue=""
                previewStyle="vertical"
                height="270px"
                initialEditType="wysiwyg"
                language="zh-CN"
                ref={editorRef}
                className="editor"
              />
            </Form.Item>
            <Form.Item>
              <Button
                disabled={!isLogin}
                type='primary'
                onClick={onSubmit}
              >
                添加评论
              </Button>
            </Form.Item>
          </>
        }
      />
      {/* 评论列表 */}
      {
        commentList?.length > 0 &&
        <List
          header="当前评论"
          dataSource={commentList}
          renderItem={(item) => (
            <Comment
              avatar={<Avatar src={item.userInfo?.avatar}></Avatar>}
              content={
                <div dangerouslySetInnerHTML={{ __html: item.commentContent }} />
              }
              datetime={
                <Tooltip title={formatDate(item.commentDate, 'year')}>
                  <span>{formatDate(item.commentDate, 'year')}</span>
                </Tooltip>
              }
            />
          )}
        />
      }
      {/* 分页 */}
    </div>
  );
}

export default Discuss;