import { makeStyles } from '@material-ui/core/styles'

export const useSharedStyles = makeStyles(theme => ({
	roundedBox: {
		padding: theme.spacing(3),
		borderRadius: theme.spacing(1),
		border: `1px solid ${theme.palette.secondary.main}`,
	},
	styledForm: {
		display: 'flex',
		flexDirection: 'column',
		justifyContent: 'space-around',
		width: '100%',
	},
	buttonDA: {
		backgroundColor: 'white',
		color: theme.palette.primary.dark,
		root: {
			'&:hover': {
				backgroundColor: theme.palette.secondary.main,
			}
		}
	},
	fullWidth: {
		width: '100%',
	}
}))

