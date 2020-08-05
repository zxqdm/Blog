import axios from 'axios'

function getCookie(name){
  let value = '; ' + document.cookie
  let parts = value.split('; ' + name + '=')
  if (parts.length === 2) return parts.pop().split(';').shift()
}


export function request(config) {
  const instance = axios.create({
    timeout: 5000
  })

  instance.interceptors.request.use(config => {
    return config
  }, error => {

  })


  instance.interceptors.response.use(response => {
    return response
  }, error => {

  })

  return instance(config)
}


