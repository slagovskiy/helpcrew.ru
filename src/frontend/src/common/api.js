import axios from 'axios'
import config from './config'

let http = axios.create()
if (localStorage.getItem('jwt_token') != null)
    http.defaults.headers.common['Authorization'] = 'JWT ' + localStorage.getItem('jwt_token')
else
    http.defaults.headers.common['Authorization'] = ''
http.defaults.headers.common['Content-Type'] = 'application/json'

const getToken =      config.BASE_URL + '/api/v1/auth/obtain_token/'
const updateToken =   config.BASE_URL + '/api/v1/auth/refresh_token/'
const userProfile =   config.BASE_URL + '/api/v1/user/profile/'
const userRegister =  config.BASE_URL + '/api/v1/user/register/'
const userPassword =  config.BASE_URL + '/api/v1/user/password/'
const userAvatar =    config.BASE_URL + '/api/v1/user/avatar/'
const userRestore =   config.BASE_URL + '/api/v1/user/restore/'
const userRestore2 =   config.BASE_URL + '/api/v1/user/restore2/'


export default {
    http,

    getToken,
    updateToken,
    userProfile,
    userRegister,
    userPassword,
    userAvatar,
    userRestore,
    userRestore2,
}
