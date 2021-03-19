import Vue from 'vue' 
import Vuex from 'vuex' 
import createPersistedState from "vuex-persistedstate"

Vue.use(Vuex)  

export default new Vuex.Store({
    state: {
      user:{},
      jwt: '' ,
      textoAnotado: "",
      idTextoAnotado: "", 
      textoAtualizado: "",
      idTextoAtualizado: "", 
      replacerList: []
    },   
    plugins: [createPersistedState()],   
    mutations: {     
      guardaTokenUtilizador(state, token) {       
        state.jwt = token;     
      },    
      guardaNomeUtilizador(state, user) {       
        state.user = user;     
      },
      updateTextoAnotado: (state, payload) => {
        Vue.set(state, "textoAnotado", payload);
      },
      updateIdTextoAnotado: (state, payload) => {
        Vue.set(state, "idTextoAnotado", payload);
      },
      updateTextoAtualizado: (state, payload) => {
        Vue.set(state, "textoAtualizado", payload);
      },
      updateIdTextoAtualizado: (state, payload) => {
        Vue.set(state, "idTextoAtualizado", payload);
      },
      updateReplacerList: (state, payload) => {
        Vue.set(state, "replacerList", payload);
      }
    },
    getters:{
      isAuthenticated (state) {
        if (!state.jwt || state.jwt.split('.').length < 3) {
          return false
        }
        const data = JSON.parse(atob(state.jwt.split('.')[1]))
        const exp = new Date(data.exp * 1000) // JS deals with dates in milliseconds since epoch
        const now = new Date()
        return now < exp
      },
      isAdmin(state){
        if(state.user.tipo != 'Admin' ){
          return false
        }
        return true
      },
      currentTextoAnotado: state => {
        return state.textoAnotado;
      },
      currentIdTextoAnotado: state => {
        return state.idTextoAnotado;
      },
      currentTextoAtualizado: state => {
        return state.textoAtualizado;
      },
      currentIdTextoAtualizado: state => {
        return state.idTextoAtualizado;
      },
      currentReplacerList: state => {
        return state.replacerList;
      }
    },
    actions: {},   
    modules: {} 
})