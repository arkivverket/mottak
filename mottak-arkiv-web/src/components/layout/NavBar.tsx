import React, { useContext } from 'react'
import { AppBar, Icon, IconButton, Theme, Toolbar, Typography } from '@material-ui/core'
import { makeStyles } from '@material-ui/core/styles'

import { LayoutContext } from './Layout'

interface StyleProps {
	drawerWidth: number | undefined
}

const useStyles = makeStyles<Theme, StyleProps>((theme: Theme) => ({
	appBar: {
		backgroundColor: theme.palette.primary.main,
		zIndex: theme.zIndex.drawer + 1,
	},
}))

const NavBar: React.FC = (): JSX.Element => {
	const { toggleDrawer, isOpen, drawerWidth } = useContext(LayoutContext)
	const classes = useStyles({ drawerWidth })

	return (
		<AppBar position="absolute" className={classes.appBar}>
			<Toolbar>
				<IconButton
					edge="start"
					color="inherit"
					aria-label={`${isOpen ? 'close' : 'open'} drawer`}
					onClick={toggleDrawer}
					className={classes.menuButton}
					data-testid="toggle-btn"
				>
					<Icon data-testid="menu-toggle-icon">{isOpen ? 'close' : 'menu'}</Icon>
				</IconButton>
				<Typography variant="h6">Mottak</Typography>
			</Toolbar>
		</AppBar>
	)
}

export default NavBar
