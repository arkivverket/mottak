import React from 'react'
import ReactDOM from 'react-dom'

import App from './App'

declare global {
	interface Window {
		_env_: any
	}
}

ReactDOM.render(
	<React.StrictMode>
		<App />
	</React.StrictMode>,
	document.getElementById('root'),
)
