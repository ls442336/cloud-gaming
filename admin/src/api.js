import axios from 'axios'

const api = axios.create({
    baseURL: process.env.REACT_APP_API_URL
})

api.interceptors.request.use(function(config) {
    const token = localStorage.getItem('token')
  
    if ( token != null ) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  
    return config;
  }, function(err) {
    return Promise.reject(err);
  });
export default api