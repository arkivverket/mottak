import * as React from 'react'
import { render, RenderResult } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import Layout from '../../components/layout/Layout'

let documentBody: RenderResult

describe('<Layout />', () => {
	beforeEach(() => {
		documentBody = render(
			<BrowserRouter>
				<Layout />
			</BrowserRouter>,
		)
	})
	it('matches snapshot', () => {
		const { baseElement } = documentBody
		expect(baseElement).toMatchSnapshot()
	})
})
