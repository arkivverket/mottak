import React from 'react'
import { BrowserRouter, Route, Switch } from 'react-router-dom'
import GlobalStyle from './styles/globalStyles'
import Layout from './components/layout/Layout'
import Routes, { RouteType } from './components/routes/Routes'
import { defaultTheme } from './styles/themes'
import { ThemeProvider } from 'styled-components'
import WorkArea from './components/WorkArea'

const App: React.FC = (): JSX.Element => (
	<ThemeProvider theme={defaultTheme}>
		<GlobalStyle />
		<BrowserRouter>
			<div>
				<Layout />
			</div>
		</BrowserRouter>
	</ThemeProvider>

)

export default App
