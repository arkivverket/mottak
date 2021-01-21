import axios from 'axios'

axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'

//axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*'

export default axios.create({
	baseURL: window?._env_?.API_BASEURL,
	timeout: 0,
	withCredentials: true,
})
