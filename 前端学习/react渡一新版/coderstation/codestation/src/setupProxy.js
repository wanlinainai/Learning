const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (app) {
  // 配置 /res 的代理
  app.use(
    '/res',
    createProxyMiddleware({
      target: 'http://localhost:7001',
      changeOrigin: true,
    })
  );

  // 配置 /api 的代理
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:7001',
      changeOrigin: true,
    })
  );

  // 配置 /static 的代理
  app.use(
    '/static',
    createProxyMiddleware({
      target: 'http://localhost:7001',
      changeOrigin: true,
    })
  );
};
