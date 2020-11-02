import React from 'react'
import { MemoryRouter, Route } from 'react-router'
import { fireEvent, render } from '@testing-library/react'
import Routes, { RouteType } from '../../components/routes/Routes'
import SideBar from '../../components/layout/SideBar'
import { LayoutContext } from '../../components/layout/Layout'

describe('<SideBar />', () => {
	it('sidebars displays routes as links', () => {
		const value = {
			toggleDrawer: jest.fn(),
			isOpen: false,
		}

		const { getByTestId, queryByText } = render(
			<MemoryRouter>
				<LayoutContext.Provider value={value}>
					<SideBar />
				</LayoutContext.Provider>
			</MemoryRouter>
		)

		Routes.map((route: RouteType) => {
			if (route.nav) {
				const link = getByTestId(route.name)
				expect(link).toBeInTheDocument()
				//TODO: check route dynamic by content
			} else {
				const linkText = queryByText(route.name)
				expect(linkText).not.toBeInTheDocument()
			}
		})
	})
})
