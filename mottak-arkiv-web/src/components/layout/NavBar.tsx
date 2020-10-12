import React, { useContext } from 'react'
import {
	AppBar,
	Icon,
	IconButton,
	Toolbar,
	Typography,
} from '@material-ui/core'
import styled from 'styled-components'
import { LayoutContext } from './Layout'

const StyledAppBar = styled(AppBar)`
	&& {
		color: ${props => props.theme.colors.white};
		background-color: ${props => props.theme.colors.black};
		z-index: 1400;
	}
`

const StyledToolBar = styled(Toolbar)`
    background-color: ${props => props.theme.colors.black};
`

const NavBar: React.FC = (): JSX.Element => {
	const { toggleDrawer, isOpen } = useContext(LayoutContext)

	return (
		<StyledAppBar position='relative'>
			<StyledToolBar>
				{!isOpen ? (
					<IconButton
						edge='start'
						color='inherit'
						aria-label='open drawer'
						onClick={toggleDrawer}
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
			</StyledToolBar>
		</StyledAppBar>
	)
}

export default NavBar
