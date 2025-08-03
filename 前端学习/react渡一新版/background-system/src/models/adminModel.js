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
    },
    addAdmin(state, { payload }) {
      const newObj = { ...state };
      newObj.adminInfo = payload;
      return newObj;
    },
    deleteAdmin(state, { payload }) {
      const newState = { ...state };
      const index = newState.adminList.indexOf(payload);
      const arr = [...state.adminList];
      arr.splice(index, 1);
      newState.adminList = arr;
      return newState;
    },

    // 更新管理员
    updateAdmin(state, { payload }) {
      const newState = { ...state };
      for (let i = 0; i < newState.adminList.length; i++) {
        if (newState.adminList[i]._id === payload.adminInfo._id) {
          for (let key in payload.newAdminInfo) {
            if (payload.newAdminInfo.hasOwnProperty(key)) {
              newState.adminList[i][key] = payload.newAdminInfo[key];
            }
          }
          break;
        }
      }
      return newState
    }
  },

  // 处理异步副作用
  effects: {
    // 初始化管理员列表
    *_initAdminList(_, { put, call }) {
      // 服务器通信
      const { data } = yield call(AdminController.getAdmin);
      // 调用 reducer 更新仓库状态
      yield put({
        type: 'initAdminList',
        payload: data
      })
    },

    // 新增管理员
    *_addAdmin({ payload }, { put, call }) {
      // 服务器通信，新增功能
      const { data } = yield call(AdminController.addAdmin, payload);
      yield put({ type: 'addAdmin', payload: data });
    },

    // 删除一个管理员
    *_deleteAdmin({ payload }, { put, call }) {
      // 服务器通信，删除功能
      yield call(AdminController.deleteAdmin, payload._id);
      // 更新本地仓库
      yield put({
        type: 'deleteAdmin',
        payload
      })
    },

    // 更新管理员信息
    *_editAdmin({ payload }, { put, call }) {
      yield call(AdminController.editAdmin, payload.adminInfo._id, payload.newAdminInfo)
      yield put({
        type: 'updateAdmin',
        payload
      })
    }
  }
}