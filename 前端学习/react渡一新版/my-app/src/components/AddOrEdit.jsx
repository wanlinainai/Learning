import { useEffect, useState } from 'react';
import { addStuApi, editStuById, getStuByIdApi } from '../api/stuApi';
import { useNavigate, useParams } from 'react-router-dom';

function AddOrEdit(props) {

  const navigate = useNavigate()

  // 根据是否有id来决定是添加和修改
  const {id} = useParams();
  
  // 创建一个受控state
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

  useEffect(() => {
    // 如果有id，需要根据该id获取用户的详细信息，并回填到表单里边
    if(id) {
      getStuByIdApi(id).then(({data}) => {
        setStu(data)
      })
    }
  }, [id])

  function updateUser(newInfo, key) {
    // console.log(newInfo, key);
    // 根据对应的Key来更新信息
    if(key ==='age' && isNaN(newInfo)) {
      return;
    }

    const newStuInfo = {...stu};
    newStuInfo[key] = newInfo.trim();
    setStu(newStuInfo);
  }


  function submitStuInfo(e) {
    e.preventDefault();

    // 发送请求
    for(const key in stu) {
      if(!stu[key]) {
        alert("请完善表单的每一项")
        return;
      }
    }

    if (id) {
      // 编辑
      editStuById(id, stu).then(() => {
        navigate("/home", {
          state: {
            alert: "学生修改成功",
            type: "info"
          }
        })
      })
    } else {
      // 新增
      addStuApi(stu).then(() => {
        // 需要做跳转
        navigate("/home", {
          state: {
            alert: "用户添加成功",
            type: "success"
          }
        })
      })
    }
  }

  return (
    <div className='contaienr'>
      <h1 className='page-header'>{id ? '修改用户': "添加用户"}</h1>
      <form id='myForm' onSubmit={submitStuInfo}>
        <div className='well'>
          <div className='form-group'>
            <label htmlFor="">姓名</label>
            <input
              type="text"
              className='form-control'
              placeholder='请填写用户名'
              value={stu.name}
              onChange={(e) => updateUser(e.target.value, "name")}
            />
          </div>

          <div className='form-group'>
            <label htmlFor="">年龄</label>
            <input
              type="text"
              className='form-control'
              placeholder='请填写用户年龄'
              value={stu.age}
              onChange={(e) => { updateUser(e.target.value, "age") }}
            />
          </div>

          <div className='form-group'>
            <label htmlFor="">联系方式</label>
            <input
              type="text"
              className='form-control'
              placeholder='请填写用户的手机号码'
              value={stu.phone}
              onChange={(e) => { updateUser(e.target.value, "phone") }}
            />
          </div>

          <div className='form-group'>
            <label htmlFor="">邮箱</label>
            <input
              type="text"
              className='form-control'
              placeholder='请填写用户的电话号码'
              value={stu.email}
            onChange={(e) => { updateUser(e.target.value, "email") }}
            />
          </div>

          <div className='form-group'>
            <label htmlFor="">学历</label>
            <select className='form-control' value={stu.education} onChange={(e) => {updateUser(e.target.value, "education")}}>
              <option >小学</option>
              <option >初中</option>
              <option >高中或技校</option>
              <option >专科</option>
              <option >本科</option>
              <option >硕士</option>
              <option >博士</option>
            </select>
          </div>

          <div className='form-group'>
            <label htmlFor="">毕业院校</label>
            <input 
              type="text"
              className='form-control'
              placeholder='请输入毕业院校'
              value={stu.graduationschool}
              onChange={(e) => {updateUser(e.target.value, "graduationschool")}}
              />
          </div>

          <div className='form-group'>
            <label htmlFor="">职业</label>
            <input 
              type="text"
              className='form-control'
              placeholder='请输入职业'
              value={stu.profession}
              onChange={(e) => {updateUser(e.target.value, "profession")}}
              />
          </div>

          <div className='form-group'>
            <label htmlFor="">个人简介</label>
            <textarea
              className='form-control'
              rows={10}
              placeholder='请简单介绍一下你自己，包括兴趣爱好等信息...'
              value={stu.profile}
            onChange={(e) => {updateUser(e.target.value, "profile")}}
            ></textarea>
          </div>

          <button type='submit' className='btn btn-primary'>{id? '确认修改': '确认添加'}</button>
        </div>
      </form>
    </div>
  );
}

export default AddOrEdit;