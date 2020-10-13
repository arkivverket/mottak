import React from 'react'
import { BrowserRouter } from 'react-router-dom'
import CssBaseline from '@material-ui/core/CssBaseline';
import Layout from './components/layout/Layout'
import { defaultTheme } from './styles/themes'
import { ThemeProvider } from '@material-ui/core/styles'

const App: React.FC = (): JSX.Element => (
	<ThemeProvider theme={defaultTheme}>
		<BrowserRouter>
			<CssBaseline />
			<Layout />
		</BrowserRouter>
	</ThemeProvider>

)

export default App
