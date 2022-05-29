import Vue from 'vue' 
import Vuex from 'vuex' 
import createPersistedState from "vuex-persistedstate"

Vue.use(Vuex)  

export default new Vuex.Store({
    state: {
      quizz_parameters: {
        domain: "",
        subdomains: [],
        id: -1,
        username: "",
        name: "",
        email: "",
        gender: "",
        degree: "",
        user_type: "",
        session_mode: ""
      },
      user:{},
      jwt: '' ,
      textoAnotado: "",
      idTextoAnotado: "", 
      textoAtualizado: "",
      idTextoAtualizado: "", 
      replacerList: [],
      drawerState: false
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
      },
      toggleDrawerState (state, data) {
        state.drawerState = data
      },set_user(state, user) {
        state.user.id = user.id
        state.user.username = user.username
        state.user.name = user.name
        state.user.email = user.email
        state.user.gender = user.gender
        state.user.degree = user.degree
        state.user.user_type = user.user_type
      },
      set_user_domains(state, domains) {
          state.user_domains = domains
      },
      set_session_domain(state, domain) {
        state.session_domain.study_cycle = domain.study_cycle
        state.session_domain.scholarity = domain.scholarity
        state.session_domain.description = domain.description
      },
      set_session_question(state, question) {
        state.session_question.content = question.content
        state.session_question.number = question.number
        state.session_question.thrown_at = question.thrown_at
      },
      set_quizz_parameters(state, quizz_parameters){
        console.log(quizz_parameters)
        state.quizz_parameters.domain = quizz_parameters.domain,
        state.quizz_parameters.subdomains = quizz_parameters.subdomains,
        state.quizz_parameters.id = quizz_parameters.id,
        state.quizz_parameters.username = quizz_parameters.username,
        state.quizz_parameters.name = quizz_parameters.name,
        state.quizz_parameters.email = quizz_parameters.email,
        state.quizz_parameters.gender = quizz_parameters.gender,
        state.quizz_parameters.degree = quizz_parameters.degree,
        state.quizz_parameters.user_type = quizz_parameters.user_type,
        state.quizz_parameters.session_mode = quizz_parameters.session_mode
      },
      set_inquiry_id(state, inquiry_id){
        state.inquiry_id = inquiry_id
      },
      async set_voice_action(state, voice_action){
        state.voice_action.advance = voice_action.advance
        state.voice_action.answer = voice_action.answer
        state.voice_action.question = voice_action.question
      },
      set_action_next(state, action_next){
        state.action_next = action_next
      },
      set_action_question(state, action_question){
        state.action_question = action_question
      },
      set_listening(state, listening){
        state.listening = listening
      },
      set_processing(state, processing){
        state.processing = processing
      },
      set_error_processing_voice(state, error_processing_voice){
        state.error_processing_voice = error_processing_voice
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
        if(state.user.type != 'Admin' ){
          return false
        }
        return true
      },
      isStudent(state){
        if(state.user.type != 'Student' ){
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
      },
      drawerState: (state) => state.drawerState

    },
    actions: {},   
    modules: {},

})