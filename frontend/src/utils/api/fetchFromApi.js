import axios from 'axios'
//import store from '../../store'

export default axios.create({
  baseURL: 'http://localhost:5000',
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
