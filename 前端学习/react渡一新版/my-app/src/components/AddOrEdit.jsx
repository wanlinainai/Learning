import { useState } from 'react';

function AddOrEdit(props) {

  // 创建一个受控state
  const [stu, setStu] = useState({
    name: "",
    age: "",
    phone: "",
    email: "",
    edcation: "本科",
    graduationschool: "",
    profession: "",
    profile: ""
  })


  function updateUser(newInfo, key) {
    // console.log(newInfo, key);
    // 根据对应的Key来更新信息
    
  }

  return (
    <div className='contaienr'>
      <h1 className='page-header'>添加用户</h1>
      <form id='myForm'>
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
            // onChange={(e) => { updateUser(e.target.value, "phone") }}
            />
          </div>

          <div className='form-group'>
            <label htmlFor="">学历</label>
            <select className='form-control' value={stu.edcation}>
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
            <label htmlFor="">个人简介</label>
            <textarea
              className='form-control'
              rows={10}
              placeholder='请简单介绍一下你自己，包括兴趣爱好等信息...'
              value={stu.profile}
            // onChange={(e) => {updateUser(e.target.value, "profile")}}
            ></textarea>
          </div>

          <button type='submit' className='btn btn-primary'>确认添加</button>
        </div>
      </form>
    </div>
  );
}

export default AddOrEdit;