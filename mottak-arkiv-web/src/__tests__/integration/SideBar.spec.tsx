import React from 'react'
import { MemoryRouter } from 'react-router'
import { render } from '@testing-library/react'
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
			</MemoryRouter>,
		)

		Routes.map((route: RouteType) => {
			if (route.nav) {
				const link = getByTestId(route.name)
				expect(link).toBeInTheDocument()
			} else {
				const linkText = queryByText(route.name)
				expect(linkText).not.toBeInTheDocument()
			}
		})
	})
})
