import axios from 'axios'
//import store from '../../store'

export default axios.create({
  baseURL: `${process.env.VUE_APP_BACKEND}`,
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json'
  }
  /*responseType:'arraybuffer',
    headers: {
        'Authorization': `Bearer: ${store.state.jwt}`
    }*/ 
})
