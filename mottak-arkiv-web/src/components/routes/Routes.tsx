import React from 'react'
import Overview from '../Overview'
import InvitationWorkflowContainer from '../workflow/InvitationWorkflowContainer'

export type RouteType = {
	path: string,
	sidebarName: string,
	component: any,
}

const Test: React.FC = () => {
	return (
		<h1>Alle</h1>
	)
}

const Routes: RouteType[] = [
	{
		path: '/',
		sidebarName: 'Oversikt',
		component: Test
	},
	{
		path: '/complete',
		sidebarName: 'Se alle',
		component: Test
	},
	{
		path: '/upload',
		sidebarName: 'Lat opp fil',
		component: Test
	},
]

export default Routes
