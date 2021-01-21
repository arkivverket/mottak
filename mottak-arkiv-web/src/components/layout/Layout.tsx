import React, { useState } from 'react'
import { makeStyles } from '@material-ui/core/styles'

import NavBar from './NavBar'
import SideBar from './SideBar'
import WorkArea from '../WorkArea'

const useStyles = makeStyles(() => ({
	root: {
		display: 'flex',
	},
}))

export type ContextType = {
	toggleDrawer: () => void
	isOpen: boolean
	drawerWidth: number
}

export const LayoutContext = React.createContext<Partial<ContextType>>({})

const Layout: React.FC = (): JSX.Element => {
	const [isOpen, setIsOpen] = useState<boolean>(false)

	const classes = useStyles()

	const drawerWidth = 240

	const toggleDrawer = () => {
		setIsOpen((prevState) => !prevState)
	}

	return (
		<LayoutContext.Provider value={{ toggleDrawer, isOpen, drawerWidth }}>
			<div className={classes.root}>
				<NavBar />
				<SideBar />
				<WorkArea />
			</div>
		</LayoutContext.Provider>
	)
}

export default Layout
