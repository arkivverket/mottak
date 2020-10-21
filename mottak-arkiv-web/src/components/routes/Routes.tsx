import React from 'react'
import Overview from '../Overview'
import InvitationWorkflowContainer from '../workflow/InvitationWorkflowContainer'

export type RouteType = {
	path: string,
	sidebarName: string,
	component: any,
	nav: boolean,
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
		component: Overview,
		nav: true,
	},
	{
		path: '/upload',
		sidebarName: 'Last opp fil',
		component: InvitationWorkflowContainer,
		nav: true,
	},
	{
		path: '/arkivutrekk',
		sidebarName: 'Se alle',
		component: All,
		nav: true,
	},
	{
		path: '/upload',
		sidebarName: 'Lat opp fil',
		component: InvitationWorkflowContainer
	},
]

export default Routes
