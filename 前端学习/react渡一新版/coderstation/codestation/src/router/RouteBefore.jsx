/**
 * 模拟导航守卫 (该组件也是一个容器组件，不做任何JSX的展示)
 */
import RouteConfig from './index.jsx';
import RouteBeforeConfig from './RouteBeforeConfig';
import { Alert } from 'antd';

function RouteBefore() {
  //获取到location.pathname 所匹配的RouteBeforeConfig对象
  const currentPath = RouteBeforeConfig.filter(item => item.path === location.pathname )[0]

  // 关闭处理
  function closeHandle() {
    location.pathname="/";
  }

  if(currentPath) {
    if(currentPath.needLogin && !localStorage.getItem("userToken")) {
      return (
        <Alert 
          message="请先登录"
          type="warning"
          closable
          onClose={closeHandle}
          style={{
                        marginTop : "30px",
                        marginBottom : "30px"
                    }}
        />
      )
    }
  }

  return <RouteConfig/>
}

export default RouteBefore;