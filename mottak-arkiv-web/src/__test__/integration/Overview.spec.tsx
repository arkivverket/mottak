import React from 'react'
import { Router } from 'react-router-dom'
import { createMemoryHistory } from 'history'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import Overview from '../../components/Overview'
import useRequest from '../../hooks/useRequest'

import '@testing-library/jest-dom/extend-expect'
import { rest } from 'msw'
import { setupServer } from 'msw/node'

jest.mock('../../hooks/useRequest.ts')

const arkivuttrekk = [{
	id: 1,
	opprettet: null,
	endret: null,
	obj_id: '1',
	status: 'Invitert',
	type: 'Noark3',
	tittel: 'En tittel',
	sjekksum_sha256: '11111',
	avgiver_navn: 'Noen',
	avgiver_epost: 'noen@stderr.no',
	koordinator_epost: 'andre@stderr.no',
	metadatafil_id: 1,
	arkiv_startdato: null,
	arkiv_sluttdato: null,
	storrelse: '1',
	avtalenummer: '1',
}]

useRequest.mockReturnValue({
	data: arkivuttrekk,
	loading: false,
	error: null,
	performRequest: jest.fn()
})

describe('<Overview />', () => {
	const server = setupServer(
		rest.get('http://localhost:8000/arkivuttrekk', (req, res, ctx) => res(ctx.json(arkivuttrekk)))
	)

	// establish API mocking before all tests
	beforeAll(() => server.listen())
	afterEach(() => server.resetHandlers())
	afterAll(() => server.close())

	it('has button that will start add new AU workflow', () => {
		const history = createMemoryHistory()
		render(
			<Router history={history}>
				<Overview />
			</Router>
		)

		const button = screen.getByText(/nytt arkivuttrekk/i)
		expect(button).toBeInTheDocument()
		fireEvent.click(button)
		expect(history.location.pathname).toBe('/arkivuttrekk/invitation')
	})


	it('loads and displays arkivuttrekk', async () => {
		const history = createMemoryHistory()
		render(
			<Router history={history}>
				<Overview />
			</Router>
		)


		await waitFor(() => screen.getByText(/en tittel/i))
	})
})
