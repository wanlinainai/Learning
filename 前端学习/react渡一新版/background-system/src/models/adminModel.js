import AdminController from '@/services/admin'


export default {
  // 命令空间
  namespace: 'admin',
  // 仓库数据
  state: {
    adminList: [], // 存储所有的管理员的信息
    adminInfo: null // 存储当前登录的管理员信息
  },
  // 同步更新仓库状态数据
  reducers: {
    initAdminList(state, { payload }) {
      // redux中规定的需要将state进行复制之后更新，否则无效
      const newState = { ...state }
      newState.adminList = payload
      return newState
    }
  },

  // 处理异步副作用
  effects: {
    *_initAdminList(_, { put, call }) {
      // 服务器通信
      const { data } = yield call(AdminController.getAdmin);
      // 调用 reducer 更新仓库状态
      yield put({
        type: 'initAdminList',
        payload: data
      })
    }
  }
}