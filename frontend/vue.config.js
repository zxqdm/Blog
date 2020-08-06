module.exports = {
  configureWebpack: {
    resolve: {
      alias: {
        'assets': '@/assets',
        'media': '@/media',
        'common': '@/common',
        'components': '@/components',
        'network': '@/network',
        'views': '@/views',
      }
    }
  },
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://39.98.207.147:8000/api',
        pathRewrite:{'^/api':''},
        ws: false,
        changeOrigin: true
      }
    }
  },
}
