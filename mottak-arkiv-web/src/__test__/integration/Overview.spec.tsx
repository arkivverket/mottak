import React from 'react'
import { Router } from 'react-router-dom'
import { createMemoryHistory } from 'history'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import Overview from '../../components/Overview'

describe('<Overview />', () => {

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


})
