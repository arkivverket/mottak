import React, { useContext } from 'react'
import {
	AppBar,
	Icon,
	IconButton,
	Theme,
	Toolbar,
	Typography,
} from '@material-ui/core'
import clsx from 'clsx'
import { makeStyles } from '@material-ui/core/styles'

import { LayoutContext } from './Layout'

interface StyleProps {
    drawerWidth: number | undefined
}

const useStyles = makeStyles<Theme, StyleProps>((theme: Theme) => ({
	toolbar: {
		paddingRight: 24, // keep right padding when drawer closed
	},
	appBar: {
		backgroundColor: theme.palette.primary.main,
		zIndex: theme.zIndex.drawer + 1,
	  },
	  menuButtonHidden: {
		display: 'none',
	  },
}))

const NavBar: React.FC = (): JSX.Element => {
	const { toggleDrawer, isOpen, drawerWidth } = useContext(LayoutContext)
	const classes = useStyles({ drawerWidth })

	return (
		<AppBar
			position='absolute'
			className={classes.appBar}
		>
			<Toolbar className={classes.toolbar}>
				{!isOpen ? (
					<IconButton
						edge="start"
						color="inherit"
						aria-label="open drawer"
						onClick={toggleDrawer}
						className={clsx(classes.menuButton, isOpen && classes.menuButtonHidden)}
				  >
						<Icon>menu</Icon>
					</IconButton>
				) : (
					<IconButton
						edge='start'
						color='inherit'
						aria-label="close drawer"
						onClick={toggleDrawer}
					>
						<Icon>close</Icon>
					</IconButton>
				)}
				<Typography variant='h6'>
                    Mottak
				</Typography>
			</Toolbar>
		</AppBar>
	)
}

export default NavBar
