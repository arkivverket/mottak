import React from 'react'
import { MemoryRouter, Route } from 'react-router'
import { fireEvent, render } from '@testing-library/react'

import Overview from '../../components/Overview'
import InvitationWorkflowContainer from '../../components/workflow/InvitationWorkflowContainer'
import WorkflowStepper from '../../components/workflow/WorkflowStepper'
import WorkArea from '../../components/WorkArea'

describe('<WorkArea />', () => {
	it('renders overview as default', async () => {
		const { getByText } = render(
			<MemoryRouter initialEntries={['/']}>
				<Route>
					<Overview />
				</Route>
			</MemoryRouter>
		)

		expect(getByText(/nytt arkivuttrekk/i)).toBeInTheDocument()
	})
	it('renders Step component', async () => {
		const { getByTestId } = render(
			<MemoryRouter initialEntries={['/upload']}>
				<Route>
					<InvitationWorkflowContainer>
						<WorkflowStepper/>
					</InvitationWorkflowContainer>
				</Route>
			</MemoryRouter>
		)

		expect(getByTestId('stepper')).toBeInTheDocument()
	})
	test('landing on a bad page', () => {
		const { getByText } = render(
			<MemoryRouter initialEntries={['/bad/route']}>
				<Route>
					<WorkArea />
				</Route>
			</MemoryRouter>
		)

		expect(getByText(/404/i)).toBeInTheDocument()
	})
})
