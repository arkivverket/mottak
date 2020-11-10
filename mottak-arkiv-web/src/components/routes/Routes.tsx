import AllArkivuttrekk from '../AllArkivuttrekk'
import Details from '../Details'
import Overview from '../Overview'
import NotFound from '../NotFound'
import InvitationWorkflowContainer from '../workflow/InvitationWorkflowContainer'

export type RouteType = {
	path: string,
	name: string,
	component: any,
	nav: boolean,
}

const Routes: RouteType[] = [
	{
		path: '/',
		name: 'Oversikt',
		component: Overview,
		nav: true,
	},
	{
		path: '/arkivuttrekk/invitation',
		name: 'Last opp fil',
		component: InvitationWorkflowContainer,
		nav: true,
	},
	{
		path: '/arkivutrekk',
		name: 'Se alle arkivuttrekk',
		component: AllArkivuttrekk,
		nav: true,
	},
	{
		path: '/arkivuttrekk/:id',
		name: 'Detaljer',
		component: Details,
		nav: false,
	},
	{
		path: '*',
		name: 'Ikke funnet',
		component: NotFound,
		nav: false,
	},
]

export default Routes
