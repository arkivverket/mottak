import React, { useEffect } from 'react'
import clsx from 'clsx'
import { makeStyles } from '@material-ui/core/styles'
import {
	Snackbar,
	SnackbarContent,
	IconButton,
	Icon,
} from '@material-ui/core'
import { AlertContent } from '../types/sharedTypes'

const useStyles = makeStyles(theme => ({
	success: {
		backgroundColor: theme.palette.success.light,
	},
	warning: {
		backgroundColor: theme.palette.warning.main,
		color: theme.palette.text.secondary,
	},
	error: {
		backgroundColor: theme.palette.error.light,
	},
	info: {
		backgroundColor: theme.palette.primary.light,
	},
	content: {
		display: 'flex',
	},
	icon: {
		marginRight: theme.spacing(1),
	},
	message: {
		display: 'flex',
		alignItems: 'center',
	},
}))

/**
 * Display alert msg.
 *
 * @param {string}  msg Message to display to the user
 * @param {string}  type type og alert; 'success', 'info', 'error' or 'warning'
 */
const Alert: React.FC<AlertContent> = ({ msg, type }): JSX.Element => {
	const [open, setOpen] = React.useState(false)
	const classes = useStyles()

	useEffect(() => {
		msg && setOpen(true)
	}, [msg])

	const handleClose = () => {
		setOpen(false)
	}

	return (
		<Snackbar
			anchorOrigin={{
				vertical: 'bottom',
				horizontal: 'center'
			}}
			open={open}
			autoHideDuration={5000}
			onClose={handleClose}
		>
			<SnackbarContent
				className={clsx(type && classes[type])}
				message={
					<div className={classes.content}>
						<Icon className={classes.icon}>{type}</Icon>
						<span className={classes.message}>{msg}</span>
					</div>
				}
				action={[
					<IconButton
						key='close'
						aria-label='Close'
						color='inherit'
						onClick={handleClose}
					>
						<Icon>close</Icon>
					</IconButton>
				]}
			/>
		</Snackbar>
	)
}
export default Alert

