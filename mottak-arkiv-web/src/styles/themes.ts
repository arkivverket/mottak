import { unstable_createMuiStrictModeTheme as createMuiTheme } from '@material-ui/core'

export const defaultTheme = createMuiTheme({
	palette: {
		primary: {
			light: '#034c6b',
			main: '#023a52',
			dark: '#022838',
		},
		secondary: {
			light: '#f2f2f2',
			main: '#e0e0e0',
			dark: '#696969',
		},
		success: {
			light: '#99d0be',
			main: '#87b8a8',
			dark: '#749e90',
		},
		info: {
			light: '#7abac8',
			main: '#6aa1ad',
			dark: '#5a8a94',
		},
		warning: {
			light: '#f2dd0f',
			main: '#d9c60d',
			dark: '#bfaf0b',
		},
		error: {
			light: '#b4080d',
			main: '#9c070b',
			dark: '#8e1d08',
		},
	},
})
