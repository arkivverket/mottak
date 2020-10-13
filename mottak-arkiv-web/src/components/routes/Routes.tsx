import React from 'react'
import Overview from '../Overview'
import InvitationWorkflowContainer from '../workflow/InvitationWorkflowContainer'

export type RouteType = {
	path: string,
	sidebarName: string,
	component: any,
}

const All: React.FC = () => {
	return (
		<h1>Alle</h1>
	)
}

const Routes: RouteType[] = [
	{
		path: '/',
		sidebarName: 'Oversikt',
		component: Overview
	},
	{
		path: '/complete',
		sidebarName: 'Se alle',
		component: All
	},
	{
		path: '/upload',
		sidebarName: 'Lat opp fil',
		component: InvitationWorkflowContainer
	},
]

export default Routes
