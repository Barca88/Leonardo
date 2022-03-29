module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
   devServer: {
   port: "8080"
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
