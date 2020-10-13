import React, { useContext } from 'react'
import { Route, Switch } from 'react-router-dom'
import Routes, { RouteType } from './routes/Routes'
import { Container, Paper, Theme } from '@material-ui/core'
import clsx from 'clsx'
import { makeStyles } from '@material-ui/core/styles'

import { LayoutContext } from './layout/Layout'

type StyleProps = {
    drawerWidth: number | undefined
}

const useStyles = makeStyles<Theme, StyleProps>((theme: Theme) => ({
	appBarSpacer: theme.mixins.toolbar,
	container: {
		paddingTop: theme.spacing(4),
		paddingBottom: theme.spacing(4),
	},
	content: {
		flexGrow: 1,
	},
	contentShift: props => ({
		transition: theme.transitions.create('margin', {
		  easing: theme.transitions.easing.sharp,
		  duration: theme.transitions.duration.leavingScreen,
		}),
		marginLeft: props.drawerWidth && -props.drawerWidth,
	}),
	contentPush: {
		transition: theme.transitions.create('margin', {
		  easing: theme.transitions.easing.easeOut,
		  duration: theme.transitions.duration.enteringScreen,
		}),
		marginLeft: 0,
	},
}))

const WorkArea: React.FC = ():JSX.Element => {
	const { toggleDrawer, isOpen, drawerWidth } = useContext(LayoutContext)
	const classes = useStyles({ drawerWidth })

	return (
		<main
			className={clsx(classes.content, isOpen ? classes.contentPush : classes.contentShift)}
		>
			<div className={classes.appBarSpacer} />
			<Container maxWidth='lg' className={classes.container}>
				<Paper elevation={2} style={{ padding: '2rem' }}>
					<Switch>
						{Routes.map((route: RouteType) => (
							<Route exact path={route.path} key={route.path}>
								<route.component />
							</Route>
						))}
					</Switch>
				</Paper>
			</Container>
		</main>
	)
}

export default WorkArea
