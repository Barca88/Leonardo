import axios from 'axios'

export default axios.create({
  baseURL: process.env.VUE_APP_TESTS_API_URL,
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json'
  }
})
