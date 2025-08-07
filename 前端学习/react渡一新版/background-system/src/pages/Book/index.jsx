import { formatDate, typeOptionCreator } from '@/utils/tools';
import { PageContainer, ProTable } from '@ant-design/pro-components';
import { useDispatch, useNavigate } from '@umijs/max';
import { Button, Popconfirm, Select, Tag } from 'antd';
import { useRef, useState } from 'react';
import { useSelector } from '@umijs/max';
import BookController from '@/services/book';

function Book(props) {

  const actionRef = useRef();
  // 分页参数
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10
  })

  const navigate = useNavigate();

  const columns = [
    {
      title: '序号',
      align: 'center',
      width: 50,
      search: false,
      render: (text, record, index) => {
        return [(pagination.current - 1) * pagination.pageSize + index + 1]
      }
    },
    {
      title: '书籍名称',
      dataIndex: 'bookTitle',
      width: 150,
      key: 'bookTitle'
    },
    {
      title: '书籍分类',
      dataIndex: 'typeId',
      key: 'typeId',
      align: 'center',
      renderFormItem: (item, {type, defaultRender, formItemProps, fieldProps, ...rest}, form) => {
        return (
          <Select placeholder="请选择查询分类" onChange={handleChange}>
            {typeOptionCreator(Select, typeList)}
          </Select>
        )
      },
      render: (_, row) => {
        // 寻找对应类型的类型名称
        const type = typeList.find((item) => item._id === row.typeId);
        return [
          <Tag color="purple" key={row.typeId}>
            {type.typeName}
          </Tag>
        ]
      }
    },
    {
      title: '书籍简介',
      dataIndex: 'bookIntro',
      key: 'bookIntro',
      align: 'center',
      search: false,
      render: (_, row) => {
        // 书籍简介进行简化，过滤掉HTML标签
        let reg = /<[^<>]+>/g;
        let brief = row.bookIntro;
        brief = brief.replace(reg, '');
        if(brief.length > 15) {
          brief = brief.slice(0, 15) + '...';
        }
        return [brief];
      }
    },
    {
      title: '书籍封面',
      dataIndex: 'bookPic',
      key: 'bookPic',
      valueType: 'image',
      align: 'center',
      search: false
    },
    {
      title: '浏览数',
      dataIndex: 'scanNumber',
      key: 'scanNumber',
      align: 'center',
      search: false
    },
    {
      title: '评论数',
      dataIndex: 'commentNumber',
      key: 'commentNumber',
      align: 'center',
      search: false
    },
    {
      title: '上架日期',
      dataIndex: 'onShelfDate',
      key: 'onShelfDate',
      align: 'center',
      search: false,
      render: (_, row) => {
        return [formatDate(row.onShelfDate)];
      }
    },
    {
      title: '操作',
      width: 150,
      key: 'option',
      valueType: 'option',
      fixed: 'right',
      align: 'center',
      render: (_, row, index, action) => {
        return [
          <div key={row._id}>
            <Button
              type='link'
              size='small'
              onClick={() => navigate(`/book/editBook/${row._id}`)}
            >
              编辑
            </Button>

            <Popconfirm
              title="是否删除该书籍以及该书籍对应的评论?"
              onConfirm={() => deleteHandle(row)}
              okText="删除"
              cancelText="取消"
            >
              <Button type='link' size='small'>
                删除
              </Button>
            </Popconfirm>
          </div>
        ]
      }
    }
  ];

  // 删除
  function deleteHandle(bookInfo) {
    BookController.deleteBook(bookInfo._id);
    actionRef.current.reload();
  }

  // 查询分类
  function handleChange(value) {
    setSearchType({
      typeId: value
    })
  }

  const dispatch = useDispatch();
  // 搜索类型
  const [searchType, setSearchType] = useState({
    typeId: null
  })

  const { typeList } = useSelector((state) => state.type);
  // 如果typeList是空，初始化
  if(!typeList.length) {
    dispatch({
      type: 'type/_initTypeList'
    })
  }

  function handlePageChange(current, pageSize) {
    setPagination({
      current,
      pageSize
    })
  }


  return (
    <>
      <PageContainer>
        <ProTable
          headerTitle="书籍列表"
          actionRef={actionRef}
          columns={columns}
          rowKey={(row) => row._id}
          params={searchType}
          onReset={() => {
            setSearchType({
              typeId: null
            })
          }}
          pagination={{
            showQuickJumper: true,
            showSizeChanger: true,
            pageSizeOptions: [5, 10, 15, 20, 25, 30],
            ...pagination,
            onChange: handlePageChange
          }}
          request={async (params) => {
            const result = await BookController.getBookByPage(params);
            return {
              data: result.data.data,
              success: !result.code,
              total: result.data.count
            }
          }}
        />
      </PageContainer>
    </>
  );
}

export default Book;