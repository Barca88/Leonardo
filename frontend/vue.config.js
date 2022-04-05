module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
   devServer: {
   proxy: 'http://localhost:5000/',
   sockPath: "sockjs-node",
   port: "8080",
   disableHostCheck: true
   },
 
  pluginOptions: {
    i18n: {
      locale: 'pt',
      fallbackLocale: 'pt',
      localeDir: 'locales',
      enableInSFC: true
    }
  }
}
