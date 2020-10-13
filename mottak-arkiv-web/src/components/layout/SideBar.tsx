import React, { useContext } from 'react'
import { NavLink, useLocation } from 'react-router-dom'
import {
	Drawer,
	ListItemText,
	MenuList,
	MenuItem,
	Theme,
	Toolbar,
} from '@material-ui/core'
import clsx from 'clsx'
import { makeStyles } from '@material-ui/core/styles'
import { LayoutContext } from './Layout'

import Routes, { RouteType } from '../routes/Routes'

type StyleProps = {
    drawerWidth: number | undefined
}

const useStyles = makeStyles<Theme, StyleProps>((theme: Theme) => ({
	toolbarIcon: {
		display: 'flex',
		alignItems: 'center',
		justifyContent: 'flex-end',
		padding: '0 8px',
		...theme.mixins.toolbar,
	},
	drawer: props => ({
		width: props.drawerWidth,
		flexShrink: 0,
	}),
	drawerPaper: props => ({
		whiteSpace: 'nowrap',
		width: props.drawerWidth,
	}),
	drawerPaperClose: {
		overflowX: 'hidden',
		transition: theme.transitions.create('width', {
			easing: theme.transitions.easing.sharp,
			duration: theme.transitions.duration.leavingScreen,
		}),
		width: theme.spacing(7),
		[theme.breakpoints.up('sm')]: {
			width: theme.spacing(9),
		},
	},
	menu: {
		color: theme.palette.primary.main,
	}
}))

const SideBar: React.FC = (): JSX.Element => {
	const { toggleDrawer, isOpen, drawerWidth } = useContext(LayoutContext)
	const classes = useStyles({ drawerWidth })

	const location = useLocation()

	const activeRoute = (routeName: string) => location?.pathname === routeName

	return (
		<Drawer
			variant='persistent'
			anchor='left'
			open={isOpen}
			className={classes.drawer}
			classes={{
				paper: clsx(classes.drawerPaper),
			}}
		>
			<Toolbar />
			<div
				role='presentation'
				onClick={toggleDrawer}
				onKeyDown={toggleDrawer}
			>
				<MenuList>
					{Routes.map((route: RouteType, key) => (
						<NavLink
							to={route.path}
							style={{ textDecoration: 'none' }}
							key={key}
							className={classes.menu}
						>
							<MenuItem selected={activeRoute(route.path)}>
								<ListItemText primary={route.sidebarName} />
							</MenuItem>
						</NavLink>
					))}
				</MenuList>
			</div>
		</Drawer>
	)
}

export default SideBar
