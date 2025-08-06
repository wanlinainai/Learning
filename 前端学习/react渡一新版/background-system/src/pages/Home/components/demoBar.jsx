import React from 'react';
import { Bar } from '@ant-design/plots';


function DemoBar(props) {
  const data = [
    {
      year: '1951年',
      value: 38
    },
    {
      year: '1952年',
      value: 52
    },
    {
      year: '1953年',
      value: 61
    },
    {
      year: '1954年',
      value: 145
    },
    {
      year: '1955年',
      value: 48
    }
  ]

  const config = {
    data,
    xField: 'value',
    yField: 'year',
    seriesField: 'year',
    legend: {
      position: 'top-left'
    }
  }
  return (
    <Bar {...config}/>
  );
}

export default DemoBar;