import React, { useState, useEffect } from 'react';
import { Pie } from '@ant-design/charts';

const DemoPie = () => {
  const data = [
    {
      type: '分类一',
      value: 27,
    },
    {
      type: '分类二',
      value: 25,
    },
    {
      type: '分类三',
      value: 18,
    },
    {
      type: '分类四',
      value: 15,
    },
    {
      type: '分类五',
      value: 10,
    },
    {
      type: '其它',
      value: 5,
    },
  ];

  const config = {
    radius: 0.9,
    appendPadding: 10,
    data,
    angleField: 'value',
    colorField: 'type',
    label: {
      type: 'inner',
      offset: '-30%',
      content: ({ type, value }) => `${type}\n${value}`,
      style: {
        fontSize: 16,
        textAlign: 'center',
      },
    },
    tooltip: {
      fields: ['type', 'value'],
      formatter: (datum) => ({
        name: datum.type,
        value: datum.value,
      }),
    },
    interactions: [{ type: 'element-active' }],
  };

  return <Pie {...config} />;
};

export default DemoPie;