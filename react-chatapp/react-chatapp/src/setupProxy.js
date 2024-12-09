const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (app) {
  app.use(
    '/api', // 프록시할 엔드포인트
    createProxyMiddleware({
      target: 'http://localhost:5000', // 백엔드 서버 주소
      changeOrigin: true,
    })
  );
};
