import axios from "axios";

const request = axios.create({
  baseURL: "http://localhost:3000",
  timeout: 5000
})

// 设置请求拦截
request.interceptors.request.use((config) => {
  // config是请求
  // 做处理
  // config.headers = 

  // 请求放行
  return config;
})


// 设置响应拦截
request.interceptors.response.use((response) => {
  // 拦截到响应
  // 对响应进行处理
  return response
}, (error) => {
  return Promise.reject(error)
})

export default request