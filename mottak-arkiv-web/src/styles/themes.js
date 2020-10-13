import { createMuiTheme } from '@material-ui/core/styles'

const colors = {
	// Greytones

	white: '#ffffff',
	whitetwo: '#fafafa',
	whitethree: '#fcfcfc',
	lightishgrey: '#f2f2f2',
	lightergrey: '#eeeeee',
	lightgrey: '#e0e0e0',
	grey: '#cccccc',
	dimgrey: '#696969',
	darkergrey: '#757575',
	darkishgrey: '#8c8c8c',
	brownishgrey: '#646464',
	darkgrey: '#444444',
	darkbluishgrey: '#373a3c',
	greyblack: '#2d2d2d',
	black: '#000000',

	// Arkivverket colors

	lightgreen: '#eff7eb',
	lightblue: '#dceff4',
	lighticeblue: '#daefef',
	iceblue: '#b6d9d6',
	darkiceblue: '#99c1c0',
	darkgreen: '#99d0be',
	blue: '#7abac8',
	darkblue: '#034c6b',
	lightred: '#e7221a',
	red: '#b4080d',
	darkred: '#8e1d08',

	// Global color styles

	primary: '#034c6b',
	primarydarker: '#023a52',
	primarydarkest: '#022838',
	success: '#99d0be',
	successdarker: '#87b8a8',
	successdarkest: '#749e90',
	warning: '#f2dd0f',
	warningdarker: '#d9c60d',
	warningdarkest: '#bfaf0b',
	info: '#7abac8',
	infodarker: '#6aa1ad',
	infodarkest: '#5a8a94',
	danger: '#b4080d',
	dangerdarker: '#9c070b',
	dangerdarkest: '#8e1d08',
	link: '#156898',
	muted: '#818a91',

	// Rgba
	overlay: 'rgba(0,0,0,0.65)',
	seethroughgrey: 'rgba(0,0,0,.2)',
}

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
	  },
})


