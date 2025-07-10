import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getStuByIdApi, deleteStuById } from '../api/stuApi';

/**
 * 学生详情组件
 * @param {} props 
 * @returns 
 */
function Detail(props) {
  // 获取动态参数
  let {id} = useParams()

  const navigate = useNavigate();

  const [stu, setStu] = useState({
     name: "",
    age: "",
    phone: "",
    email: "",
    education: "本科",
    graduationschool: "",
    profession: "",
    profile: ""
  })

  // 根据该id获取详细信息
  useEffect(() => {
    getStuByIdApi(id).then(({data}) => {
      setStu(data);
      
    })
  }, [id])

  function deleteUser(id) {
    if(window.confirm("真的删除吗？删除无法回退欧")) {
      deleteStuById(id).then(() => {
        navigate("/home", {
          state: {
            alert: "用户删除成功",
            type: "info"
          }
        })
      })
    }
  }
  
  return (
    <div className='details container'>
      <button className='btn btn-default' onClick={() => {navigate("/home")}}>返回</button>
      <h1 className='page-header'>
        {stu.name}
        <span className='pull-right'>
          <button className='btn btn-primary' style={{marginRight: 10}} onClick={() => {navigate(`/edit/${stu.id}`)}}>修改</button>
          <button className='btn btn-danger' onClick={() => {deleteUser(stu.id)}}>删除</button>
        </span>
      </h1>

      <ul className='list-group'>
        <li className='list-group-item'>
          <span className='glyphicon glyphicon-phone'>电话：{stu.phone}</span>
        </li>
        <li className='list-group-item'>
          <span className='glyphicon glyphicon-envelope'>邮箱：{stu.email}</span>
        </li>
      </ul>

      <ul className='list-group'>
        <li className='list-group-item'>
          <span className='glyphicon glyphicon-book'>文化水平：{stu.education}</span>
        </li>
        <li className='list-group-item'>
          <span className='glyphicon glyphicon-flag'>毕业院校：{stu.graduationschool}</span>
        </li>
        <li className='list-group-item'>
          <span className='glyphicon glyphicon-briefcase'>专业：{stu.profession}</span>
        </li>
        <li className='list-group-item'>
          <span className='glyphicon glyphicon-user'>个人简介：{stu.profile}</span>
        </li>
      </ul>
    </div>
  );
}

export default Detail;