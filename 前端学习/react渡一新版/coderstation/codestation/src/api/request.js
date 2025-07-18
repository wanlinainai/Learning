import axios from "axios";

const service = axios.create({
  timeout: 5000
})


// 请求拦截
service.interceptors.request.use((config) => {
  // 拦截到请求之后u，可以做一些事情
  const token = localStorage.getItem('userToken');
  if(token) {
    config.headers['Authorization'] = "Bearer " + token;
  }
  // 放行
  return config;
}, (err) => {
  // 发生错误的回调函数
  console.log("请求拦截出错，错误信息:", err)
});

// 响应拦截
service.interceptors.response.use((response) => {
  const res = response.data;
  // 放行
  return res;
}, (err) => {
  // 发生错误的回调函数
  console.log("响应拦截出错，错误信息:", err)
})

export default service;