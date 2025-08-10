import { PageContainer, ProTable } from '@ant-design/pro-components';
import React, { useState, useRef } from 'react';

import InterviewController from '@/services/interview';
import { Button, message, Popconfirm, Select, Tag } from 'antd';
import { typeOptionCreator, formatDate } from '@/utils/tools';
import { useDispatch, useSelector } from '@umijs/max';
import { useNavigate } from 'react-router-dom';

function Interview(props) {

  const navigate = useNavigate();
  const dispatch = useDispatch();
  const actionRef = useRef();

  const [searchType, setSearchType] = useState({
    typeId: null
  });

  const { typeList } = useSelector((state) => state.type);
  if (!typeList.length) {
    dispatch({
      type: 'type/_initTypeList'
    })
  }

  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10
  })

  function handlePageChange(current, pageSize) {
    setPagination({
      current,
      pageSize
    })
  }

  function handleChange(value) {
    setSearchType({
      typeId: value
    })
  }

  /**
   * 删除功能
   */
  function deleteHandle(interviewInfo) {
    InterviewController.deleteInterview(interviewInfo._id);
    actionRef.current.reload();
    message.success('删除题目成功')
  }

  const columns = [
    {
      title: '序号',
      align: 'center',
      width: 50,
      search: false,
      render: (text, record, index) => {
        return [(pagination.current - 1) * pagination.pageSize + index + 1];
      }
    },
    {
      title: '题目名称',
      dataIndex: 'interviewTitle',
      key: 'interviewTitle',
      render: (_, row) => {
        let brief = null;
        if (row.interviewTitle.length > 22) {
          brief = row.interviewTitle.slice(0, 22) + "...";
        } else {
          brief = row.interviewTitle;
        }
        return [brief];
      }
    },
    {
      title: '题目分类',
      dataIndex: 'typeId',
      key: 'typeId',
      align: 'center',
      renderFormItem: (
        item,
        { type, defaultRender, formItemProps, fieldProps, ...rest },
        form
      ) => {
        return (
          <Select placeholder='请选择查询类型' onChange={handleChange}>
            {typeOptionCreator(Select, typeList)}
          </Select>
        )
      },
      render: (_, row) => {
        const type = typeList.find((item) => item._id === row.typeId);
        return [
          <Tag color='purple' key={row.typeId}>
            {type.typeName}
          </Tag>
        ]
      }
    },
    {
      title: '上架时间',
      dataIndex: 'onSchelfDate',
      key: 'onShelfDate',
      align: 'center',
      search: false,
      render: (_, row) => {
        return [formatDate(row.onShelfDate)];
      }
    },
    {
      title: '操作',
      width: 200,
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
              onClick={() => navigate(`/interview/interviewDetail/${row._id}`)}
            > 详情 </Button>
            <Button
              type='link'
              size='small'
              onClick={() => navigate(`/interview/editInterview/${row._id}`)}
            >
              编辑
            </Button>
            <Popconfirm
              title='确认删除该面试题吗？'
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
  ]
  return (
    <div>
      <PageContainer>
        <ProTable
          headerTitle='题目列表'
          columns={columns}
          params={searchType}
          actionRef={actionRef}
          rowKey={(row) => row._id}
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
            const result = await InterviewController.getInterviewByPage(params);
            return {
              data: result.data.data,
              success: !result.code,
              total: result.data.count
            }
          }}
        />
      </PageContainer>
    </div>
  );
}

export default Interview;