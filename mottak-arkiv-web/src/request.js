import axios from 'axios'

export default axios.create({
	baseURL: window?._env_?.API_BASEURL,
	timeout: 0,
	credentials: 'same-origin'
})
