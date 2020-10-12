import React, { useState } from 'react'
import NavBar from './NavBar'
import SideBar from './SideBar'
import WorkArea from '../WorkArea'

export type ContextType = ({
	toggleDrawer: () => void,
	isOpen: boolean,
})

export const LayoutContext = React.createContext<Partial<ContextType>>({})

const Layout: React.FC = (): JSX.Element => {
	const [isOpen, setIsOpen] = useState<boolean>(false)

	const toggleDrawer = () => {
		console.warn('toggle', isOpen);

		// if (
		// 	event.type === 'keydown' &&
		// 	((event as React.KeyboardEvent).key === 'Tab' ||
		//     (event as React.KeyboardEvent).key === 'Shift')
		// ) {
		// 	return
		// }

		setIsOpen(prevState => !prevState)
	}

	return (
		<LayoutContext.Provider value={{ toggleDrawer, isOpen }}>
			<NavBar />
			<div>
				<SideBar />
				<WorkArea />
			</div>
		</LayoutContext.Provider>
	)
}

export default Layout
