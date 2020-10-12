import React, { useContext } from 'react'
import { NavLink, useLocation } from 'react-router-dom'
import {
	Drawer,
	ListItemText,
	MenuList,
	MenuItem,
	Toolbar,
} from '@material-ui/core'
import styled from 'styled-components'
import { LayoutContext } from './Layout'

import Routes, { RouteType } from '../routes/Routes'

const StyledMenuItem = styled(MenuItem)`
  &&& {
    padding: ${props => props.theme.spacing.xs} ${props => props.theme.spacing.xl};
  }
`
const StyledDrawer = styled(Drawer)`
    position: 'relative';
    width: 240;
    `

const SideBar: React.FC = (): JSX.Element => {
	const { toggleDrawer, isOpen } = useContext(LayoutContext)
	const location = useLocation()

	const activeRoute = (routeName: string) => location?.pathname === routeName

	return (
		<StyledDrawer
			variant='persistent'
			anchor='left'
			open={isOpen}
			onClose={toggleDrawer}
		>
			<Toolbar />
			<div
				role='presentation'
				onClick={toggleDrawer}
				onKeyDown={toggleDrawer}
			>
				<MenuList>
					{Routes.map((route: RouteType, key) => {
						return (
							<NavLink to={route.path} style={{ textDecoration: 'none' }} key={key}>
								<StyledMenuItem selected={activeRoute(route.path)}>
									<ListItemText primary={route.sidebarName} />
								</StyledMenuItem>
							</NavLink>
						)
					})}
				</MenuList>
			</div>
		</StyledDrawer>
	)
}

export default SideBar
