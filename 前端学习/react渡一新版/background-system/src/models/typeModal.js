import TypeController from '@/services/type';


/**
 * Type类型模态框
 */
export default {
  namespace: 'type',
  state: {
    typeList: []
  },
  reducers: {
    initTypeList: (state, { payload }) => {
      const newState = { ...state };
      newState.typeList = payload;
      return newState;
    }
  },

  effects: {
    // 初始化类型列表
    *_initTypeList(_, { put, call }) {
      const { data } = yield call(TypeController.getType)
      // 调用reducer更新本地仓库
      yield put({
        type: 'initTypeList',
        payload: data
      })
    }
  }
}