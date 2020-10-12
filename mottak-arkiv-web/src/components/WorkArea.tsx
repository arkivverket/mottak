import React from 'react'
import { Route, Switch } from 'react-router-dom'
import Routes, { RouteType } from './routes/Routes'
import { Container, Paper } from '@material-ui/core'
import styled from 'styled-components'

const StyledContainer = styled(Container)`
   margin: ${props => props.theme.spacing.lg} 0;
`

// type Props = {
// 	children: JSX.Element | JSX.Element[]
// }

const WorkArea: React.FC = ():JSX.Element => {
	return (
		<StyledContainer maxWidth='lg'>
			<Paper elevation={2} style={{ padding: '2rem' }}>
				<Switch>
					{Routes.map((route: RouteType) => (
						<Route exact path={route.path} key={route.path}>
							<route.component />
						</Route>
					))}
				</Switch>
			</Paper>
		</StyledContainer>
	)
}

export default WorkArea
