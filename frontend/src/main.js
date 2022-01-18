import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import 'vuetify/dist/vuetify.min.css'
import VueMaterial from 'vue-material'
import PrettyCheckbox from 'pretty-checkbox-vue';
import Print from "vue-print-nb";
import VueRouter from 'vue-router'
import VueMeta from 'vue-meta'
import VueHtmlToPaper from "vue-html-to-paper";


import i18n from './i18n'
import router from './router'
import store from './store'
import axios from 'axios'



const options = {
  name: "_blank",
  specs: ["fullscreen=yes", "titlebar=yes", "scrollbars=yes"],
  styles: [
    "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css",
    "https://unpkg.com/kidlat-css/css/kidlat.css"
  ]
};

Vue.config.productionTip = false;
Vue.use(VueHtmlToPaper, options);
Vue.use(PrettyCheckbox);
Vue.use(Print);
Vue.use(VueMeta);
Vue.use(vuetify);
Vue.use(VueMaterial);
Vue.use(VueRouter);



// register jw pagination component globally
import JwPagination from 'jw-vue-pagination';
Vue.component('jw-pagination', JwPagination);

Vue.config.productionTip = false

// router.beforeEach((to, from, next) =>{
//   //language from route param or default
//   let language = to.params.lang
//   if(!language){
//     language='pt'
//   }

//   //set current lang
//   i18n.locale = language
//   next()
// })

Vue.prototype.$http = axios

const token = localStorage.getItem('token')
if (token) {
  Vue.prototype.$http.defaults.headers.common['Authorization'] = token
}

new Vue({

  router,
  store,
  vuetify,
  i18n,
  render: h => h(App)
}).$mount('#app')
