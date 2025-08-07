import { defineConfig } from '@umijs/max';

export default defineConfig({
  antd: {},
  access: {},
  model: {},
  initialState: {},
  request: {},
  layout: {
    title: 'code station',
  },
  dva: {}, // 打开dva插件
  routes: [
    {
      path: '/',
      redirect: '/home',
    },
    {
      name: '首页',
      path: '/home',
      component: './Home',
      icon: 'HomeOutlined'
    },
    {
      name: '管理员',
      path: '/admin',
      icon: "SafetyCertificateOutlined",
      routes: [{
        name: '管理员列表',
        path: 'adminList',
        component: './Admin'
      }, {
        name: '添加管理员',
        path: 'addAdmin',
        component: './Admin/addAdmin'
      }
      ]
    },
    {
      name: '用户',
      path: '/user',
      icon: 'UserOutlined',
      routes: [
        {
          name: '用户列表',
          path: 'userList',
          component: './User'
        }, {
          name: '添加用户',
          path: 'addUser',
          component: './User/addUser'
        }
      ]
    },
    {
      name: '书籍',
      path: '/book',
      icon: 'BookOutlined',
      routes: [
        {
          name: '书籍列表',
          path: 'bookList',
          component: './Book'
        }, {
          name: '添加书籍',
          path: 'addBook',
          component: './Book/addBook'
        },
        {
          name: '编辑书籍',
          path: 'editBook/:id',
          component: './Book/editBook',
          hideInMenu: true
        }
      ]
    },
    {
      name: '面试题',
      path: '/interview',
      icon: 'QuestionOutlined',
      routes: [
        {
          name: '面试题列表',
          path: 'interviewList',
          component: './Interview'
        }, {
          name: '添加面试题',
          path: 'addInterview',
          component: './Interview/addInterview'
        }
      ]
    },
    {
      name: "问答",
      path: "/issue",
      icon: 'FormOutlined',
      routes: [
        {
          name: '问答列表',
          path: 'issueList',
          component: './Issue'
        },
        {
          name: '添加问答',
          path: 'addIssue',
          component: './Issue/addIssue'
        }
      ]
    },
    {
      name: '评论',
      path: "/comment",
      icon: 'CommentOutlined',
      routes: [
        {
          name: '评论列表',
          path: 'commentList',
          component: './Comment'
        },
        {
          name: '添加评论',
          path: 'addComment',
          component: './Comment/addComment'
        }
      ]
    },
    {
      name: '类型',
      path: "/type",
      component: './Type',
      icon: 'BarsOutlined'
    }
  ],
  proxy: {
    '/api': {
      target: 'http://localhost:7001',
      changeOrigin: true
    },
    '/static': {
      target: 'http://localhost:7001',
      changeOrigin: true,
    },
    '/res': {
      target: 'http://localhost:7001',
      changeOrigin: true,
      pathRewrite: { '^/res': '' }
    }
  },
  npmClient: 'npm',
});

