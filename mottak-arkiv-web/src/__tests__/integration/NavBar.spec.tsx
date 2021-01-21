import * as React from 'react'
import { fireEvent, render, screen } from '@testing-library/react'
import NavBar from '../../components/layout/NavBar'
import { LayoutContext } from '../../components/layout/Layout'

describe('<NavBar />', () => {
	it('toggleDrawer is called when user clicks on menu-icon', () => {
		const value = {
			toggleDrawer: jest.fn(),
			isOpen: false,
		}

		render(
			<LayoutContext.Provider value={value}>
				<NavBar />
			</LayoutContext.Provider>,
		)
		expect(screen.getByTestId('toggle-btn')).toBeInTheDocument()

		expect(screen.getByText('menu')).toBeInTheDocument()

		fireEvent.click(screen.getByTestId('toggle-btn'))

		expect(value.toggleDrawer).toHaveBeenCalledTimes(1)
	})
	it('if menu is open close-icon should be displayed', () => {
		const value = {
			toggleDrawer: jest.fn(),
			isOpen: true,
		}

		render(
			<LayoutContext.Provider value={value}>
				<NavBar />
			</LayoutContext.Provider>,
		)

		expect(screen.getByText('close')).toBeInTheDocument()
	})
})
